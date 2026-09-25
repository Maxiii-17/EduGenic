# EduGenie 🧠✨ — Google Gemini Powered Learning Assistant

A lightweight AI-powered educational assistant that simplifies learning through generative AI.
Built with **FastAPI** (backend) + **HTML/CSS/JS** (frontend), powered by **Google Gemini**.

## Features

| Feature | Endpoint | Description |
|---|---|---|
| ❓ Q&A | `GET /qa?question=...` | Smart, concise answers to any question |
| 📖 Explain | `POST /explain/` | Simple concept explanations (local LaMini-Flan-T5 if installed, else Gemini) |
| 📝 Summarize | `POST /summarize/` | Condense long passages for quick revision |
| 🎯 Quiz | `POST /quiz` | 3 MCQs × 4 options with instant ✅/❌ checking |
| 🗺️ Learning path | `GET /learn/recommendations?topic=...` | Beginner → advanced plan with timelines & resources |

## Quick start (Windows)

```powershell
cd "EduGenie Google Gemini Powered Learning Assistant"
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# edit .env and paste your key from https://aistudio.google.com/app/apikey
python -m uvicorn main:app --reload
```

Or simply double-click **`run.bat`** — it starts the server and opens the app.

Then open **http://127.0.0.1:8000** (don't open `index.html` directly — CSS and APIs need the server).

## Project structure

```
EduGenie/
├── main.py                # FastAPI app + routes
├── ai_client.py           # Provider dispatcher (ollama -> gemini -> pollinations)
├── gemini_client.py       # Google Gemini (model fallback chain)
├── ollama_client.py       # Local unlimited AI via Ollama
├── pollinations_client.py # Keyless cloud fallback
├── qna.py                 # Question answering
├── explanation_module.py  # Concept explanation (local model w/ Gemini fallback)
├── quiz_module.py         # Quiz generation (JSON output)
├── summary_module.py      # Summarization
├── learning_path.py       # Learning recommendations
├── templates/index.html   # Frontend
├── static/style.css       # Styling
├── requirements.txt
├── run.bat                # One-click Windows launcher
└── .env.example           # Copy to .env and add your GEMINI_API_KEY
```

## Configuration (`.env`)

```
GEMINI_API_KEY=your_key_here   # optional if Ollama is running
GEMINI_MODEL=gemini-3.6-flash
AI_PROVIDER=auto               # auto = ollama -> gemini -> pollinations
OLLAMA_MODEL=qwen2.5:1.5b
```

## AI providers (no key? no problem)

| Provider | Key? | Quota? | Quality | Setup |
|---|---|---|---|---|
| 🦙 Ollama (local) | none, private | **unlimited** | good (1–3B models) | `winget install Ollama.Ollama`, then `ollama pull qwen2.5:1.5b` and keep `ollama serve` running |
| ✨ Gemini | API key | ~20 req/day/model | best | key from https://aistudio.google.com/app/apikey |
| 🌐 Pollinations | none | generous | basic | nothing — automatic last resort |

`AI_PROVIDER=auto` (default) tries Ollama first, then Gemini (with model fallback
`3.6-flash → 3.5-flash → flash-latest → 3-flash-preview` on 404/429/503), then
Pollinations. Set `AI_PROVIDER=ollama` for fully private, unlimited, offline AI.

> ⚠️ Never commit your real `.env` — it's already in `.gitignore`.

## Optional: fully-local explanations

```powershell
python -m pip install "transformers>=4.40" torch
```

This enables the `MBZUAI/LaMini-Flan-T5-783M` model (~3 GB download) for the
Explain feature, as in the original project spec. Without it, explanations use Gemini.

## API docs

With the server running: **http://127.0.0.1:8000/docs** (auto-generated Swagger UI).

## Deploy on Vercel

1. Go to **vercel.com → Add New… → Project → Import** the `EduGenic` repo.
2. In **Environment Variables**, add `GEMINI_API_KEY` (your key) and optionally
   `GEMINI_MODEL` (default `gemini-3.6-flash`).
3. Deploy — Vercel uses `vercel.json` + `api/index.py` (FastAPI via Mangum).

> Notes: Netlify can't host this (static-only, no Python backend). On Vercel's free
> tier requests time out after ~60s, so Q&A/Quiz/Summary are fine but the long
> Learning-Path call may occasionally need a retry.
