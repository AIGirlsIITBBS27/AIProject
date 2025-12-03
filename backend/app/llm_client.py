# app/llm_client.py


import os
import openai

OPENAI_KEY = os.getenv("OPENAI_API_KEY")  
if OPENAI_KEY:
    openai.api_key = OPENAI_KEY


def generate_with_openai(question, facts):
    prompt_facts = "\n".join([f"- {f['disease']}: {f.get('info','')}" for f in facts])
    prompt = f"""You are a helpful medical assistant for patients. Keep language simple and explain facts.
Question: {question}

Relevant facts:
{prompt_facts}

Answer (brief, patient-friendly, include evidence used):
"""
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}],
        max_tokens=200,
        temperature=0.2
    )
    return resp['choices'][0]['message']['content'].strip()


from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer


_HF_PIPE = None
def _get_hf_pipe():
    global _HF_PIPE
    if _HF_PIPE is None:
       
        model_name = "google/flan-t5-small"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        _HF_PIPE = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
    return _HF_PIPE

def generate_with_hf(question, facts):
    facts_text = " ".join([f["disease"] + ": " + f.get("info","") for f in facts])
    prompt = f"Question: {question}\nFacts: {facts_text}\nAnswer (simple):"
    pipe = _get_hf_pipe()
    out = pipe(prompt, max_length=150, num_return_sequences=1)
    return out[0]['generated_text']
