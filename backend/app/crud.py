"""
CRUD and ORM models for Judicia.ai

This file supports both:
- being imported as a package (recommended): `from .db import Base, SessionLocal`
- being run directly for quick tests: `python crud.py`
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime

# Try package-style import first; fallback to plain module import if run directly
try:
    # when imported as part of package (uvicorn backend.app.main:app)
    from .db import Base, SessionLocal, engine
except Exception:
    # when executed directly (python crud.py) — adjust path so import works
    import sys
    from pathlib import Path

    THIS_DIR = Path(__file__).resolve().parent
    if str(THIS_DIR) not in sys.path:
        sys.path.insert(0, str(THIS_DIR))

    # now import db from the same folder
    from db import Base, SessionLocal, engine  # type: ignore

# ---------------------------------
# SQLAlchemy ORM Models
# ---------------------------------

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=True)
    message = Column(Text)
    response = Column(Text)
    ts = Column(DateTime, default=datetime.utcnow)


class Documents(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    content = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.utcnow)


# ---------------------------------
# Helper functions
# ---------------------------------

def init_db(engine_arg):
    """
    Create tables if they do not exist.
    Keep engine passed in to avoid tight coupling.
    """
    Base.metadata.create_all(bind=engine_arg)


def save_chat(session, user_id, message, response):
    """
    Save a chat message + response to database.
    """
    ch = ChatHistory(
        user_id=user_id,
        message=message,
        response=response
    )
    session.add(ch)
    session.commit()
    session.refresh(ch)
    return ch


def save_document(session, filename, content):
    """
    Save uploaded document with extracted content.
    """
    doc = Documents(
        filename=filename,
        content=content
    )
    session.add(doc)
    session.commit()
    session.refresh(doc)
    return doc


# -------------------------------------------------------
# Quick smoke test when running this file directly:
# python backend/app/crud.py   (from project root use -m or run from folder)
# -------------------------------------------------------
if __name__ == "__main__":  # quick local test (not for production)
    print("Running quick CRUD smoke test...")
    # Create tables using the engine we imported
    try:
        init_db(engine)
        print("✅ Tables created (or already exist).")
    except Exception as e:
        print("❌ Failed to create tables:", e)

    # Example: open a session and insert a tiny test row
    try:
        session = SessionLocal()
        ch = save_chat(session, user_id=1, message="hello test", response="ok")
        print("✅ Saved chat id =", ch.id)
    except Exception as e:
        print("❌ DB insert failed:", e)
    finally:
        try:
            session.close()
        except Exception:
            pass
