"""Summary Module — summarizes long text using Gemini."""
from gemini_client import generate_gemini_text


def summarize_text(text: str) -> str:
    try:
        prompt = f"Summarize the following text in simple language:\n\n{text}"
        return generate_gemini_text(prompt)
    except Exception as e:  # noqa: BLE001
        return f"⚠️ Error in Summary: {e}"
