"""Ollama provider — free, private, unlimited. Runs on your own machine.

Setup (one time):
  1. Install Ollama: https://ollama.com/download  (or: winget install Ollama.Ollama)
  2. Pull a small model:  ollama pull qwen2.5:1.5b
  3. That's it — no API key, no quota, works offline.

Pick model via OLLAMA_MODEL env (e.g. llama3.2:1b, qwen2.5:1.5b, llama3.2:3b).
"""
import json
import os
import urllib.request

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")


def _post(path: str, payload: dict, timeout: int = 180) -> dict:
    req = urllib.request.Request(
        OLLAMA_HOST + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def is_available() -> bool:
    try:
        urllib.request.urlopen(OLLAMA_HOST + "/api/tags", timeout=3).read()
        return True
    except Exception:  # noqa: BLE001 — Ollama not installed/running
        return False


def generate(prompt: str) -> str:
    data = _post(
        "/api/generate",
        {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
    )
    text = (data.get("response") or "").strip()
    if not text:
        raise RuntimeError(f"Ollama ({OLLAMA_MODEL}) returned empty text.")
    return text
