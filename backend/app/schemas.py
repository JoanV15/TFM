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

    # 🔍 Métricas automáticas Opik (LLM-as-a-Judge)
    hallucination: Optional[float] = None
    moderation: Optional[float] = None
    context_precision: Optional[float] = None
    context_recall: Optional[float] = None
    usefulness: Optional[float] = None
    answer_relevance: Optional[float] = None
    g_eval: Optional[float] = None

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

# Esquemas para métricas heurísticas
class HeuristicMetricsRequest(BaseModel):
    expected_output: str
    actual_output: str

class HeuristicMetricsResponse(BaseModel):
    equals: bool
    contains: bool
    regexmatch: bool
    isjson: bool
    levenshtein: float
