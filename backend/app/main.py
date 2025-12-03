# # app/main.py

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware

from app import database, models
from app.auth import router as auth_router
from app.medical_chatbot import process_user_message

app = FastAPI(title="KG-MedQA Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB tables (MySQL)
models.Base.metadata.create_all(bind=database.engine)

# ---------- Auth routes ----------
app.include_router(auth_router)


# ---------- Chat / ask endpoint ----------
@app.post("/ask")
async def ask(payload: dict = Body(...)):
    """
    Main chat endpoint for the frontend.

    Accepts:
    {
        "question": "...",
        OR "message": "...",
        OR "query": "..."
    }
    """

    question = (
        payload.get("question")
        or payload.get("message")
        or payload.get("query")
    )

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Missing 'question' field in request"
        )

    result = process_user_message(question)

    return {
        "question_original": question,
        "answer": result.get("answer"),
        "symptoms": result.get("symptoms", []),
        "kg_results": result.get("kg_results", []),
        "triage_questions": result.get("triage_questions", []),
        "facts_used": result.get("kg_results", []),
        "detected_language": "auto"
    }


@app.get("/")
def home():
    return {"msg": "KG-MedQA backend is running successfully 🚀"}
