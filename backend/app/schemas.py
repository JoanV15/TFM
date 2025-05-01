from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class InteractionBase(BaseModel):
    id: str
    parent_id: Optional[str] = None
    role: str  # 'user' o 'assistant'
    content: str
    model: Optional[str] = None
    timestamp: Optional[datetime] = None
    rating: Optional[int] = None
    tags: Optional[List[str]] = None
    feedback_id: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class InteractionCreate(BaseModel):
    role: str
    content: str
    model: Optional[str] = None
    timestamp: Optional[datetime] = None
    rating: Optional[int] = None
    tags: Optional[List[str]] = None
    feedback_id: Optional[str] = None

class EvaluationUpdate(BaseModel):
    score: Optional[float] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    
class InteractionOut(InteractionBase):
    pass
