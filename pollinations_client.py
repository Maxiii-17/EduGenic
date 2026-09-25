"""Pollinations provider — free cloud AI, no API key needed.

Keyless fallback so the app (including the Vercel deployment) works with
zero setup. Basic open models; quality is lower than Gemini/Ollama-3b,
but fine for Q&A, summaries and quizzes.
"""
import urllib.parse
import urllib.request

MODEL = "openai"


def generate(prompt: str, timeout: int = 120) -> str:
    encoded = urllib.parse.quote(prompt, safe="")
    url = f"https://text.pollinations.ai/{encoded}?model={MODEL}"
    req = urllib.request.Request(url, headers={"User-Agent": "EduGenie/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        text = resp.read().decode("utf-8").strip()
    if not text:
        raise RuntimeError("Pollinations returned empty text.")
    return text
