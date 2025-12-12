# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .utils import save_upload_file, extract_text_from_pdf
from .model import model
from .db import SessionLocal, engine
from .crud import init_db, save_chat, save_document, ChatHistory
from .schemas import ChatRequest, ChatResponse, UploadResponse
import os

app = FastAPI(title='Judicia.ai API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure DB tables exist
init_db(engine)


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    session: Session = SessionLocal()
    try:
        prompt = req.message

        # Call the model (ModelBackend.predict returns {"output": "..."} on success)
        reply_obj = model.predict(prompt)

        if isinstance(reply_obj, dict) and "output" in reply_obj:
            reply = reply_obj["output"]
        else:
            # Fallback: stringify whatever model returned
            reply = str(reply_obj)

        # Save into MySQL
        save_chat(session, req.user_id, prompt, reply)

        return {"reply": reply}

    except Exception as e:
        # Provide helpful error message for debugging
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        session.close()


@app.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    filename = file.filename

    # Save the raw file to disk
    path = save_upload_file(file_bytes=contents, filename=filename)

    # Extract text
    if filename.lower().endswith(".pdf"):
        content_text = extract_text_from_pdf(path)
    else:
        try:
            content_text = contents.decode("utf-8")[:10000]
        except:
            content_text = "[binary file]"

    session = SessionLocal()
    try:
        save_document(session, filename, content_text)
    finally:
        session.close()

    return {
        "filename": filename,
        "content_preview": content_text[:1000]
    }


@app.get("/history")
def get_history(limit: int = 50):
    session = SessionLocal()

    try:
        q = (
            session.query(ChatHistory)
            .order_by(ChatHistory.id.desc())
            .limit(limit)
            .all()
        )

        return [
            {
                "id": row.id,
                "user_id": row.user_id,
                "message": row.message,
                "response": row.response,
                "ts": row.ts.isoformat(),
            }
            for row in q
        ]

    finally:
        session.close()
