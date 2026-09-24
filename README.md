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
├── gemini_client.py       # Shared Gemini client (model fallback, friendly errors)
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
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.6-flash
```

The client automatically fails over across `gemini-3.6-flash → gemini-3.5-flash →
gemini-flash-latest → gemini-3-flash-preview` on retired models (404), exhausted
free-tier quota (429) or overload (503).

> ⚠️ Never commit your real `.env` — it's already in `.gitignore`. The free tier
> allows ~20 requests/day per model; quota errors reset daily.

## Optional: fully-local explanations

```powershell
python -m pip install "transformers>=4.40" torch
```

This enables the `MBZUAI/LaMini-Flan-T5-783M` model (~3 GB download) for the
Explain feature, as in the original project spec. Without it, explanations use Gemini.

## API docs

With the server running: **http://127.0.0.1:8000/docs** (auto-generated Swagger UI).
