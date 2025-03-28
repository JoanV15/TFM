from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InteractionCreate(BaseModel):
    prompt: str
    response: str
    thumbs: Optional[str] = "none"

class InteractionEval(BaseModel):
    eval_score: int
    eval_tags: Optional[str]
    eval_notes: Optional[str]

class InteractionOut(BaseModel):
    id: int
    prompt: str
    response: str
    thumbs: str
    created_at: datetime
    eval_score: Optional[int]
    model_config = {
        "from_attributes": True  
    }
