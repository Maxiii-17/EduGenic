"""QnA Module — answers questions via dispatcher (ollama -> gemini -> pollinations)."""
from ai_client import generate_text


def answer_question_with_gemini(question: str) -> str:
    try:
        return generate_text(question)
    except Exception as e:  # noqa: BLE001
        return f"⚠️ Error in QnA: {e}"
