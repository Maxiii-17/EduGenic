"""Explanation Module — LaMini-Flan-T5-783M locally, Gemini fallback.

PDF spec: MBZUAI/LaMini-Flan-T5-783M via transformers+torch.
The local model (~3GB) is loaded lazily and only if the libraries are
installed. Otherwise we fall back to Gemini so the app still works.
"""
import os

MODEL_ID = "MBZUAI/LaMini-Flan-T5-783M"

_tokenizer = None
_model = None
_local_failed_reason = ""


def _try_load_local():
    global _tokenizer, _model, _local_failed_reason
    if _model is not None:
        return True
    if os.getenv("EDUGENIE_EXPLAIN_LOCAL", "1") == "0":
        _local_failed_reason = "disabled via EDUGENIE_EXPLAIN_LOCAL=0"
        return False
    try:
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)
        return True
    except Exception as e:  # noqa: BLE001 — torch/transformers missing, no net, etc.
        _local_failed_reason = str(e)
        _tokenizer = None
        _model = None
        return False


def _explain_local(topic: str) -> str:
    import torch

    input_text = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
    inputs = _tokenizer(input_text, return_tensors="pt")
    with torch.no_grad():
        outputs = _model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            do_sample=True,
        )
    return _tokenizer.decode(outputs[0], skip_special_tokens=True)


def explain_topic(topic: str) -> str:
    if _try_load_local():
        try:
            return _explain_local(topic)
        except Exception as e:  # noqa: BLE001
            print(f"Local explanation failed, falling back to Gemini: {e}")
    # Fallback: dispatcher (Ollama local -> Gemini -> Pollinations)
    try:
        from ai_client import generate_text

        prompt = (
            f"Explain the concept of '{topic}' in a simple and clear way "
            f"for a school student. Keep it concise and easy to understand."
        )
        text = generate_text(prompt)
        if _local_failed_reason:
            print(f"Note: local model unavailable ({_local_failed_reason}); used Gemini.")
        return text
    except Exception as e:  # noqa: BLE001
        return f"⚠️ Error in Explanation: {e}"
