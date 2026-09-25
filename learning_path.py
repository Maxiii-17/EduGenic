"""Learning Path Module — structured beginner→advanced plan via Gemini."""
from gemini_client import generate_gemini_text


def get_learning_recommendations(topic: str):
    prompt = f"""You are an AI tutor. The student wants to learn about: {topic}.
Suggest a structured and adaptive learning path including key topics, order of learning, and resources (videos, articles, books).
Include beginner, intermediate, and advanced levels if needed.
For each level give: estimated time, key topics, and recommended resources.
End with 4-6 adaptive learning tips."""
    try:
        return generate_gemini_text(prompt)
    except Exception as e:  # noqa: BLE001
        print(f"Learning-path error: {e}")
        return f"❌ Error occurred: {e}"
