import os, json, time
from openai import OpenAI
from dotenv import load_dotenv
from main import get_system_prompt

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")

candidates = [
    "meta-llama/llama-3.2-3b-instruct:free",
    "mistralai/mistral-small-3.2-24b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "google/gemma-3-27b-it:free",
    "qwen/qwen-2.5-72b-instruct:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
]

sys_prompt = get_system_prompt()
tests = ["whats his specialization in btech", "what tech stack did he use in the Plant Brain project"]

for model in candidates:
    print("\n=== MODEL:", model, "===")
    try:
        for q in tests:
            msgs = [{"role":"system","content":sys_prompt},{"role":"user","content":q}]
            t = time.time()
            comp = client.chat.completions.create(model=model, messages=msgs,
                response_format={"type":"json_object"}, temperature=0.3, max_tokens=400)
            dt = time.time()-t
            content = comp.choices[0].message.content
            ok = False
            try:
                json.loads(content); ok = True
            except Exception:
                ok = False
            print(f"  [{dt:.1f}s] JSON_OK={ok} len={len(content or '')} -> {repr((content or '')[:180])}")
    except Exception as e:
        print("  ERROR:", str(e)[:200])
