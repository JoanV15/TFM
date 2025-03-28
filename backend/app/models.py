from sqlalchemy import Column, Integer, String, Text, DateTime
from .database import Base
from datetime import datetime

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text)
    response = Column(Text)
    thumbs = Column(String)  # "up", "down", "none"
    created_at = Column(DateTime, default=datetime.utcnow)
    lamb_metadata = Column(Text)  # JSON serializado
    eval_score = Column(Integer, nullable=True)
    eval_tags = Column(Text, nullable=True)
    eval_notes = Column(Text, nullable=True)
