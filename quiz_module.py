"""Quiz Module — generates 3 MCQs (4 options each) as JSON via dispatcher."""
import json
import re

from ai_client import generate_text


def clean_json_block(text: str) -> str:
    """Remove Markdown ```json code fences."""
    return re.sub(r"```(?:json)?\n(.*?)```", r"\1", text, flags=re.DOTALL).strip()


def generate_quiz(text: str) -> list:
    try:
        prompt = f'''You are a quiz generator.

From the following passage, create 3 multiple-choice questions. Each question should include:
- A "question"
- A list of 4 "options"
- A correct "answer" that must exactly match one of the options.

Format your output as **valid JSON**, like this:
[
  {{
    "question": "What is ...?",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]
Return ONLY the JSON array, no other text.

Passage:
{text}
'''
        quiz_text = generate_text(prompt)
        cleaned_text = clean_json_block(quiz_text)
        parsed = json.loads(cleaned_text)
        if not isinstance(parsed, list):
            return [{"error": f"Unexpected quiz format: {quiz_text[:500]}"}]
        return parsed
    except json.JSONDecodeError as e:
        return [{"error": f"Could not parse quiz JSON: {e}. Raw: {quiz_text[:500]}"}]
    except Exception as e:  # noqa: BLE001
        return [{"error": f"⚠️ Error in Quiz: {e}"}]
