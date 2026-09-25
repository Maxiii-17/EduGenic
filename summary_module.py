"""Summary Module — summarizes long text via dispatcher."""
from ai_client import generate_text


def summarize_text(text: str) -> str:
    try:
        prompt = f"Summarize the following text in simple language:\n\n{text}"
        return generate_text(prompt)
    except Exception as e:  # noqa: BLE001
        return f"⚠️ Error in Summary: {e}"
