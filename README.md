# AI Portfolio - Jagadeesh Arigala

Interactive AI portfolio for Jagadeesh Arigala.

## Stack

- Frontend: React, TypeScript, Vite, Tailwind CSS, Framer Motion
- Backend: FastAPI, Python, Groq
- Knowledge base: `backend/knowledge_base.md`

## Local Run

Backend:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Frontend uses:

```env
VITE_API_URL=http://localhost:8000
```

Backend uses:

```env
GROQ_API_KEY=your_groq_key
```

## Deploy

Backend on Render:

```text
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

Frontend on Vercel:

```text
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
```

Set Vercel environment variable:

```env
VITE_API_URL=https://your-render-backend-url
```
