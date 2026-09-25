"""AI dispatcher — tries providers in order, first success wins.

AI_PROVIDER env:
  auto         ollama -> gemini -> pollinations   (default)
  ollama       local only (private, unlimited, needs Ollama running)
  gemini       Google Gemini only (needs GEMINI_API_KEY)
  pollinations keyless cloud only (no setup)
"""
import os

from dotenv import load_dotenv

load_dotenv()

AI_PROVIDER = os.getenv("AI_PROVIDER", "auto").strip().lower()


def _try_ollama(prompt: str) -> str:
    import ollama_client

    if not ollama_client.is_available():
        raise RuntimeError("Ollama not running (start it with: ollama serve).")
    return ollama_client.generate(prompt)


def _try_gemini(prompt: str) -> str:
    from gemini_client import generate_gemini_text

    return generate_gemini_text(prompt)


def _try_pollinations(prompt: str) -> str:
    import pollinations_client

    return pollinations_client.generate(prompt)


_CHAINS = {
    "ollama": [_try_ollama],
    "gemini": [_try_gemini],
    "pollinations": [_try_pollinations],
    "auto": [_try_ollama, _try_gemini, _try_pollinations],
}


def generate_text(prompt: str) -> str:
    chain = _CHAINS.get(AI_PROVIDER, _CHAINS["auto"])
    errors = []
    for fn in chain:
        try:
            return fn(prompt)
        except Exception as e:  # noqa: BLE001 — try next provider
            errors.append(str(e)[:150])
    raise RuntimeError("All AI providers failed — " + " | ".join(errors))
