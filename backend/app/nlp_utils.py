# app/nlp_utils.py
import json
from ollama import Client

client = Client()

def translate_to_en(text: str):
    """Translate text to English using Ollama (mistral)."""
    prompt = f"""
Translate this text to English only. 
Return ONLY the translated sentence:

{text}
"""
    try:
        r = client.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        translated = r["message"]["content"].strip()
        return translated, "auto"
    except:
        return text, "en"


def translate_from_en(text: str, target_lang: str):
    """Translate English back to target language."""
    if target_lang == "en" or target_lang == "auto":
        return text

    prompt = f"""
Translate this English text to {target_lang}.
Return ONLY the translated sentence:

{text}
"""
    try:
        r = client.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        return r["message"]["content"].strip()
    except:
        return text


def detect_language(text: str):
    """Dummy detector (optional) — always returns auto."""
    return "auto"
