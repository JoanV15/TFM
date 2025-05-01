from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class InteractionBase(BaseModel):
    id: str
    parent_id: Optional[str] = None
    prompt: str
    response: str
    model: Optional[str] = None
    timestamp: Optional[datetime] = None
    rating: Optional[int] = None
    score: Optional[int] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    chat_title: Optional[str] = None
    feedback_id: Optional[str] = None
    usage: Optional[Dict] = None
    chat_id: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class InteractionCreate(BaseModel):
    prompt: str
    response: str
    model: Optional[str] = None
    timestamp: Optional[datetime] = None
    rating: Optional[int] = None
    score: Optional[int] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    chat_title: Optional[str] = None
    feedback_id: Optional[str] = None
    usage: Optional[Dict] = None
    parent_id: Optional[str] = None
    chat_id: Optional[str] = None

class EvaluationUpdate(BaseModel):
    rating: Optional[int] = None
    score: Optional[int] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None

class InteractionOut(InteractionBase):
    pass
