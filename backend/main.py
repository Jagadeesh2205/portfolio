import os
import json
import re
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Portfolio Brain")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the LLM client.
# Preference order: OpenRouter (OpenAI-compatible) -> Groq -> local fallback.
# Put OPENROUTER_API_KEY (or GROQ_API_KEY) in your .env file.
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

# Which provider is active: "openrouter", "groq", or None (local fallback).
if openrouter_api_key:
    client = OpenAI(
        api_key=openrouter_api_key,
        base_url="https://openrouter.ai/api/v1",
    )
    provider = "openrouter"
    # OPENROUTER_MODEL may be a comma-separated list. Free models live on shared
    # upstream pools that intermittently return 429/404, so we try each in order
    # and only fall back to the local keyword responder if every model fails.
    _default_models = (
        "nvidia/nemotron-nano-9b-v2:free,"
        "openai/gpt-oss-20b:free,"
        "nvidia/nemotron-3-super-120b-a12b:free,"
        "google/gemma-4-31b-it:free"
    )
    model_list = [m.strip() for m in os.getenv("OPENROUTER_MODEL", _default_models).split(",") if m.strip()]
    model_name = model_list[0] if model_list else None
elif groq_api_key:
    client = Groq(api_key=groq_api_key)
    provider = "groq"
    model_name = "llama-3.3-70b-versatile"
    model_list = [model_name]
else:
    client = None
    provider = None
    model_name = None
    model_list = []

class ChatMessageModel(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str
    history: list[ChatMessageModel] = []

class ChatResponse(BaseModel):
    intent: str
    ai_text: str

# Base prompt layout
BASE_SYSTEM_PROMPT = """You are Jagadeesh Arigala's AI Portfolio Assistant. Your job is to answer questions about Jagadeesh based on the provided Knowledge Base and determine what UI component the frontend should render.

Knowledge Base:
======================
{knowledge_base}
======================

Your response MUST be valid JSON matching this schema exactly:
{{
  "intent": "me" | "projects" | "resume" | "skills" | "contact" | "general",
  "ai_text": "Your natural, conversational response speaking as Jagadeesh's assistant."
}}

Rules:
- CRITICAL INTENT ROUTING RULES:
  * Set intent to "me" ONLY when the user asks a general intro query like "Tell me about yourself", "Who are you", or "Introduction".
  * If the user asks about specific details (such as CGPA, GPA, grades, marks, specific project explanations like "explain Plant Brain", or specific technology details), set intent to "general" and answer the question directly in text.
  * If the user explicitly asks to view, show, list, or see all projects or portfolio, set intent to "projects".
  * If the user asks to explain or detail a specific project (e.g. "explain Plant Brain", "tell me about Diabetic Retinopathy Detection", "how does the WhatsApp bot work"), set intent to "general" and provide a thorough technical explanation without showing the full project carousel again.
  * If the user asks about CGPA or GPA, set intent to "general" and state clearly: "Jagadeesh's B.Tech CGPA in Computer Science & Engineering (AI & ML Specialization) at VIT-AP University is 8.51 / 10.0."
  * If the user asks about work experience or resume timeline, set intent to "resume".
  * If the user asks about skills or certifications, set intent to "skills".
  * If the user wants contact info, set intent to "contact".
- Keep `ai_text` friendly, professional, concise, and structured.
- CRITICAL Punctuation Rule: Always write English contractions with proper apostrophes (e.g. use "I've", "I'm", "don't", "it's", "you're", "we've", "they're").
"""

def get_system_prompt() -> str:
    try:
        kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base.md")
        with open(kb_path, "r", encoding="utf-8") as f:
            kb_content = f.read()
        return BASE_SYSTEM_PROMPT.format(knowledge_base=kb_content)
    except Exception as e:
        print(f"Error loading knowledge base: {e}")
        return BASE_SYSTEM_PROMPT.format(knowledge_base="Knowledge base file not found.")

def match_known_answer(query: str):
    """Return a confident canned ChatResponse for well-covered topics, else None.

    Used as an instant fast-path (before hitting the LLM) so nav-intent and
    known-topic queries answer immediately and correctly, and as the source of
    truth for the local fallback when the LLM is unavailable or fails.
    """
    q = query.lower()

    # CGPA / Education specific queries
    if any(word in q for word in ["cgpa", "gpa", "marks", "percentage", "score", "rank"]):
        return ChatResponse(
            intent="general",
            ai_text="Jagadeesh's B.Tech CGPA in Computer Science & Engineering (AI & ML) at VIT-AP University is 8.51 / 10.0. He scored 95.9% in Intermediate (Narayana Junior College, EAPCET Rank: 8001) and 594/600 in Class 10 (Keshava Reddy School)."
        )

    # Specialization / branch queries
    if "specialization" in q or "specialize" in q or "specialisation" in q or ("branch" in q and any(w in q for w in ["btech", "b.tech", "degree", "engineering"])):
        return ChatResponse(
            intent="general",
            ai_text="Jagadeesh's B.Tech specialization is Computer Science & Engineering with an Artificial Intelligence & Machine Learning (AI & ML) focus, at VIT-AP University, Amaravati (2022–2026)."
        )

    # Specific Project Explanations
    if "plant brain" in q or "hybrid graph" in q:
        return ChatResponse(
            intent="general",
            ai_text="Plant Brain is an industrial knowledge intelligence platform built for ET Techathon 2026. It converts complex industrial manuals and logs into a queryable knowledge system using Hybrid Graph-RAG (combining ChromaDB vector search with NetworkX knowledge graph traversal). It serves 3 specialized AI agents (Expert Copilot, Maintenance RCA, and Compliance Analyzer), reducing information retrieval time from 23 minutes to 3 seconds."
        )

    if "diabetic" in q or "retinopathy" in q or "fundus" in q:
        return ChatResponse(
            intent="general",
            ai_text="The Diabetic Retinopathy Detection project automates 5-grade DR severity grading from retinal fundus images. Built with TensorFlow/Keras, it features a lightweight MobileNetV3Small backbone augmented with a CBAM (Convolutional Block Attention Module) spatial and channel attention layer to focus on microaneurysms and exudates. It achieved 89% accuracy on APTOS 2019 and 83% cross-dataset generalization on 50,000+ EyePACS images."
        )

    if "skin" in q or "dermoscopy" in q:
        return ChatResponse(
            intent="general",
            ai_text="The Skin Disease Classification project is a multi-class CNN classifier built during an internship at Infosys Springboard. Trained across 27,000 dermoscopy images across 9 disease categories, it achieved 94% test accuracy and a Macro-F1 score of 0.91. It is containerized with Docker and deployed via a Flask REST API."
        )

    if "whatsapp" in q or "booking" in q:
        return ChatResponse(
            intent="general",
            ai_text="The WhatsApp Appointment Booking System is a stateless webhook-driven scheduling platform built with Node.js and Twilio WhatsApp Business API. When a user messages, intent is parsed, written to a Supabase PostgreSQL database, and an instant confirmation reply is sent back via WhatsApp."
        )

    # General Education
    if any(word in q for word in ["education", "university", "study", "college", "school", "vit", "narayana"]):
        return ChatResponse(
            intent="general",
            ai_text="Jagadeesh is pursuing B.Tech in CSE (AI & ML Specialization) at VIT-AP University, Amaravati (2022–2026, GPA: 8.51/10). He completed Intermediate at Narayana Junior College, Tirupati (95.9%, EAPCET Rank: 8001) and Class X at Keshava Reddy School, Tirupati (594/600)."
        )

    # Explicit Projects list trigger
    if any(word in q for word in ["projects", "show projects", "list projects", "view projects", "portfolio"]):
        return ChatResponse(
            intent="projects",
            ai_text="I have loaded Jagadeesh's project portfolio above, including Plant Brain (Hybrid Graph-RAG AI platform), Diabetic Retinopathy Detection (MobileNetV3 + CBAM), Skin Disease Classifier (Infosys Springboard), and WhatsApp Appointment Booking System."
        )

    # Skills trigger
    if any(word in q for word in ["skill", "stack", "technology", "python", "tensorflow", "pytorch", "certif"]):
        return ChatResponse(
            intent="skills",
            ai_text="Jagadeesh's core skills include Python, TensorFlow, OpenCV, LangChain, ChromaDB, FastAPI, React 18, Docker, and Azure AI. He holds Oracle GenAI, Oracle Data Science, Azure AI-900, AWS Cloud, and CS50P certifications."
        )

    # Experience / Resume trigger
    if any(word in q for word in ["experience", "resume", "work", "job", "career", "intern", "internship", "ethara", "teachnook", "infosys"]):
        return ChatResponse(
            intent="resume",
            ai_text=(
                "Jagadeesh has three roles across his career so far:\n\n"
                "1. Data Annotation & LLM Evaluator — Ethara AI (Mar 2026 – May 2026): structured data annotation for LLM training pipelines and post-training LLM response evaluation (quality, accuracy, instruction-following).\n"
                "2. AI & ML Intern — Infosys Springboard (Nov 2024 – Jan 2025, Remote): built a multi-class CNN skin-disease classifier reaching 94% accuracy across 9 categories on 27,000 images, using MLOps practices (experiment tracking, versioning, Docker).\n"
                "3. ML Intern — Teachnook (2023 – 2024): implemented core ML algorithms from scratch and with Scikit-learn (regression, classification, clustering) on real datasets."
            )
        )

    # Contact trigger
    if any(word in q for word in ["contact", "email", "linkedin", "github", "phone", "reach"]):
        return ChatResponse(
            intent="contact",
            ai_text="You can reach Jagadeesh at arigalajagadeesh@gmail.com or +91 77805 88637. LinkedIn: linkedin.com/in/jagadeesharigala | GitHub: github.com/Jagadeesh2205."
        )

    # General Intro trigger ONLY for generic about/intro queries
    if any(word in q for word in ["about yourself", "who are you", "tell me about yourself", "who is jagadeesh"]):
        return ChatResponse(
            intent="me",
            ai_text="You can see a quick summary of Jagadeesh Arigala's background above. Ask about his Hybrid Graph-RAG system (Plant Brain), computer vision models, or internship experience."
        )

    # No confident match — let the caller decide (LLM, or generic fallback).
    return None


def get_local_response(query: str) -> ChatResponse:
    """Offline responder: a confident canned answer, or a friendly generic prompt."""
    known = match_known_answer(query)
    if known is not None:
        return known
    return ChatResponse(
        intent="general",
        ai_text="I can help you explore Jagadeesh Arigala's AI/ML profile, projects, skills, experience, education, certifications, and contact details."
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Fast-path: well-covered topics (about, projects, skills, experience, CGPA,
    # education, contact, known projects) answer instantly from verified data —
    # no LLM round-trip, so no latency and no risk of a weak model hallucinating.
    instant = match_known_answer(request.query)
    if instant is not None:
        return instant

    if not client:
        return get_local_response(request.query)

    system_prompt = get_system_prompt()

    messages = [{"role": "system", "content": system_prompt}]

    # Append conversation history
    for msg in request.history:
        role = "user" if msg.role == "user" else "assistant"
        messages.append({"role": role, "content": msg.content})

    # Append latest user query
    messages.append({"role": "user", "content": request.query})

    # Try each configured model in order. Free models share upstream pools that
    # intermittently return 429/404, so one being unavailable shouldn't drop us
    # to the local keyword responder — only exhausting the whole list does.
    data = None
    last_error = None
    for candidate in model_list:
        try:
            completion = client.chat.completions.create(
                model=candidate,
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.3,
                max_tokens=700  # room for full JSON; 200 truncated multi-line answers mid-object
            )

            response_content = completion.choices[0].message.content
            if not response_content or not response_content.strip():
                # Model returned empty content (some free models spend the budget
                # on internal reasoning); try the next candidate.
                raise ValueError("empty completion content")

            # Some free models emit multi-line answers with raw (unescaped)
            # newlines inside the JSON string, which strict parsing rejects.
            # strict=False tolerates control characters; if the object is still
            # malformed (e.g. wrapped in prose or a code fence), salvage the
            # first {...} block.
            try:
                data = json.loads(response_content, strict=False)
            except json.JSONDecodeError:
                match = re.search(r"\{.*\}", response_content, re.DOTALL)
                if not match:
                    raise
                data = json.loads(match.group(0), strict=False)

            break  # success — stop trying further models
        except Exception as e:
            last_error = e
            print(f"AI model '{candidate}' failed, trying next (provider={provider}): {e}")
            continue

    if data is None:
        print(f"All AI models failed; using local fallback (provider={provider}): {last_error}")
        return get_local_response(request.query)

    try:
        ai_text = data.get("ai_text", "I'm not quite sure how to answer that.")
        
        # Post-process to restore missing apostrophes in common contractions
        ai_text = re.sub(r"\b[Ii]ve\b", "I've", ai_text)
        ai_text = re.sub(r"\b[Ii]m\b", "I'm", ai_text)
        ai_text = re.sub(r"\b[Dd]ont\b", "don't", ai_text)
        ai_text = re.sub(r"\b[Cc]ant\b", "can't", ai_text)
        ai_text = re.sub(r"\b[Yy]oure\b", "you're", ai_text)
        ai_text = re.sub(r"\b[Ww]eve\b", "we've", ai_text)
        ai_text = re.sub(r"\b[Tt]heyre\b", "they're", ai_text)
        
        return ChatResponse(
            intent=data.get("intent", "general"),
            ai_text=ai_text
        )
        
    except Exception as e:
        print(f"AI backend fallback used (provider={provider}): {e}")
        return get_local_response(request.query)

@app.get("/")
async def root():
    return {
        "message": "Hello from the AI Portfolio Backend!",
        "provider": provider or "local-fallback",
        "model": model_name,
    }
