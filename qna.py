"""QnA Module — answers questions using Gemini (PDF: Gemini 1.5 Pro)."""
from gemini_client import generate_gemini_text


def answer_question_with_gemini(question: str) -> str:
    try:
        return generate_gemini_text(question)
    except Exception as e:  # noqa: BLE001
        return f"⚠️ Error in QnA: {e}"
