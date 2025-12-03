import os
import json
import re
import traceback
from neo4j import GraphDatabase


NEO4J_USER = "neo4j"
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "Surbhi@123")
KG_DB = "kgmap"

USE_OLLAMA = True
OLLAMA_MODEL = "mistral"

conversation_history = []       
pending_triage_questions = []   
triage_answers = {}             


client_ollama = None
if USE_OLLAMA:
    try:
        from ollama import Client
        client_ollama = Client()
    except Exception as e:
        print("[ollama] Failed to create client:", e)
        traceback.print_exc()
        client_ollama = None


def create_driver_try():
    uris = ["bolt://127.0.0.1:7687", "neo4j://127.0.0.1:7687"]
    for uri in uris:
        try:
            d = GraphDatabase.driver(uri, auth=(NEO4J_USER, NEO4J_PASSWORD))
            with d.session(database=KG_DB) as s:
                if s.run("RETURN 1 AS one").single()["one"] == 1:
                    return d
        except:
            continue
    return None

driver = create_driver_try()

def search_kg(symptoms):
    if driver is None:
        results = []
        for s in symptoms:
            results.append({
                "symptom": s.capitalize(),
                "possible_diseases": ["Viral Infection", "Dehydration", "Migraine"]
                if s.lower() in ["fever", "headache"] else ["Unknown"]
            })
        return results

    query = """
    MATCH (s:SymptomNode)
    WHERE toLower(s.name) IN $symptoms
    OPTIONAL MATCH (s)<-[r:CAUSES]-(d:DiseaseNode)
    RETURN s.name AS symptom, collect(d.name) AS possible_diseases
    """
    with driver.session(database=KG_DB) as session:
        return session.run(query, symptoms=[x.lower() for x in symptoms]).data()


def decompose_question(user_query):
    conversation_history.append({"role": "user", "content": user_query})
    if client_ollama is None:
        return [user_query]
    prompt = f"""Break this medical query into sub-questions ONLY if needed: "{user_query}".
    Output strictly JSON list like ["sub1","sub2"]."""
    try:
        resp = client_ollama.chat(model=OLLAMA_MODEL, messages=[{"role":"user","content":prompt}])
        txt = resp.get("message",{}).get("content","").replace("```json","").replace("```","").strip()
        if txt.startswith("["): return json.loads(txt)
        return [user_query]
    except:
        return [user_query]

def extract_entities_llm(user_msg):
    fallback_keywords = {"knee":"knee pain","head":"headache","fever":"fever"}
    if client_ollama is None:
        return {"symptoms": [v for k,v in fallback_keywords.items() if k in user_msg.lower()]}
    prompt = f"""Extract symptoms from: "{user_msg}" as JSON: {{"symptoms":["symptom1"]}}"""
    try:
        resp = client_ollama.chat(model=OLLAMA_MODEL, messages=[{"role":"user","content":prompt}])
        match = re.search(r'\{.*\}', resp.get("message",{}).get("content",""), re.DOTALL)
        return json.loads(match.group()) if match else {"symptoms":[]}
    except:
        return {"symptoms":[]}


def generate_triage_questions_llm(symptoms):
    if not symptoms: return []
    prompt = f"""Patient reported: {symptoms}. Generate 3 clear questions. JSON list only."""
    try:
        resp = client_ollama.chat(model=OLLAMA_MODEL, messages=[{"role":"user","content":prompt}])
        text = resp.get("message",{}).get("content","").replace("```json","").replace("```","").strip()
        questions = json.loads(text)
        if isinstance(questions,list) and all(isinstance(q,str) for q in questions): return questions
        raise ValueError("Invalid format")
    except:
        return [
            f"Where exactly do you feel the {symptoms[0]}?",
            f"How long have you been experiencing the {symptoms[0]}?",
            f"Does anything make the {symptoms[0]} better or worse?"
        ]


def doctor_style_reply_llm(user_query, kg_results, all_symptoms):
    if client_ollama is None:
        return "Let’s continue. Tell me more."
    conversation_history.append({"role":"user","content":user_query})
    system_prompt = "You are a helpful medical doctor. Answer empathetically based on symptoms only."
    msgs = [{"role":"system","content":system_prompt}]
    msgs.extend(conversation_history[-8:])
    msgs.append({"role":"user","content":f"Symptoms: {all_symptoms}\nKG info: {kg_results}"})
    try:
        resp = client_ollama.chat(model=OLLAMA_MODEL, messages=msgs)
        ans = resp.get("message",{}).get("content","")
        conversation_history.append({"role":"assistant","content":ans})
        return ans
    except:
        return "I'm here with you. Can you tell me more about your symptoms?"


def process_user_message(user_query: str):
    """
    Returns structured dict: 
    { answer, symptoms, kg_results, triage_questions }
    This is what the FastAPI /ask endpoint sends to the frontend.
    """
    global pending_triage_questions, triage_answers


    if pending_triage_questions:
        user_answers = [a.strip() for a in user_query.split(",")]

        for ans in user_answers:
            if pending_triage_questions:
                q = pending_triage_questions.pop(0)
                triage_answers[q] = ans
                conversation_history.append({
                    "role": "user_answer",
                    "question": q,
                    "answer": ans
                })

        if pending_triage_questions:
            return {
                "answer": None,
                "symptoms": list(triage_answers.values()),
                "kg_results": [],
                "triage_questions": pending_triage_questions,
            }

        all_symptoms = list(triage_answers.values())
        kg_results = search_kg(all_symptoms)
        final_answer = doctor_style_reply_llm(user_query, kg_results, all_symptoms)

        triage_answers.clear()

        return {
            "answer": final_answer,
            "symptoms": all_symptoms,
            "kg_results": kg_results,
            "triage_questions": []
        }

    subqs = decompose_question(user_query)

    all_symptoms = []
    for sq in subqs:
        all_symptoms.extend(extract_entities_llm(sq).get("symptoms", []))

    all_symptoms = list(set(all_symptoms))

    if not all_symptoms:
        return {
            "answer": "Please describe your main symptom.",
            "symptoms": [],
            "kg_results": [],
            "triage_questions": []
        }

    triage_qs = generate_triage_questions_llm(all_symptoms)

    if triage_qs:
        pending_triage_questions = triage_qs
        return {
            "answer": "To understand your symptoms better, please answer the following questions.",
            "symptoms": all_symptoms,
            "kg_results": [],
            "triage_questions": triage_qs
        }

    kg_results = search_kg(all_symptoms)
    final_answer = doctor_style_reply_llm(user_query, kg_results, all_symptoms)

    return {
        "answer": final_answer,
        "symptoms": all_symptoms,
        "kg_results": kg_results,
        "triage_questions": []
    }
