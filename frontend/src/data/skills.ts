export interface SkillCategory {
  title: string;
  description: string;
  icon: string;
  skills: string[];
  color: string;
}

export const skillsData: SkillCategory[] = [
  {
    title: "AI, ML & Deep Learning",
    description: "Building production ML models, attention architectures, CNNs, and computer vision pipelines.",
    icon: "Brain",
    skills: ["Python", "TensorFlow", "Keras", "PyTorch", "OpenCV", "CBAM Attention", "MobileNetV3", "CNNs", "Scikit-learn"],
    color: "bg-violet-50 border-violet-100 text-violet-700"
  },
  {
    title: "LLMs, GenAI & RAG Systems",
    description: "Designing Hybrid Graph-RAG architectures, multi-agent frameworks, and vector search pipelines.",
    icon: "Workflow",
    skills: ["LangChain", "ChromaDB", "Graph-RAG", "NetworkX", "spaCy NER", "ONNX Runtime", "Azure AI Foundry", "Groq API", "FAISS"],
    color: "bg-indigo-50 border-indigo-100 text-indigo-700"
  },
  {
    title: "Web Development & APIs",
    description: "Developing responsive microservices, REST APIs, and modern frontend interfaces.",
    icon: "Code",
    skills: ["FastAPI", "Flask", "Node.js", "React 18", "TypeScript", "Vite", "REST APIs", "WebSocket Streaming"],
    color: "bg-emerald-50 border-emerald-100 text-emerald-700"
  },
  {
    title: "Databases & Storage",
    description: "Managing relational databases, vector storage, and knowledge graphs.",
    icon: "Database",
    skills: ["MySQL", "PostgreSQL", "Supabase", "ChromaDB", "FAISS", "NetworkX Graph"],
    color: "bg-amber-50 border-amber-100 text-amber-700"
  },
  {
    title: "Cloud, MLOps & DevOps",
    description: "Containerizing applications, setting up CI/CD pipelines, and deploying to cloud infrastructure.",
    icon: "Server",
    skills: ["Docker", "GitHub Actions", "Azure App Service", "Vercel", "AWS Cloud", "Git", "Postman"],
    color: "bg-sky-50 border-sky-100 text-sky-700"
  },
  {
    title: "Verified Certifications",
    description: "Industry-recognized credentials in Cloud, Generative AI, Data Science, and Python.",
    icon: "Tool",
    skills: [
      "Oracle Generative AI Professional",
      "Oracle Data Science Professional",
      "Microsoft Azure AI-900",
      "AWS Cloud Foundations",
      "AWS Cloud Architecting",
      "CS50P Python (Harvard)",
      "Cisco Python Essentials",
      "TCS_iON Career Edge"
    ],
    color: "bg-rose-50 border-rose-100 text-rose-700"
  }
];
