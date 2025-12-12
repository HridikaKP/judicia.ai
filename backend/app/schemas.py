from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    user_id: Optional[int]
    message: str
    top_k: Optional[int] = 5


class ChatResponse(BaseModel):
    reply: str


class UploadResponse(BaseModel):
    filename: str
    content_preview: str
