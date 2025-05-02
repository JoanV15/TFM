from sqlalchemy import Column, String, Text, Integer, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import JSON

Base = declarative_base()

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(String, primary_key=True, index=True)  # ID único de respuesta
    parent_id = Column(String, nullable=True)          # ID del mensaje padre
    prompt = Column(Text, nullable=False)              # Texto del usuario
    response = Column(Text, nullable=False)            # Respuesta del modelo
    model = Column(String, nullable=True)              # Modelo usado
    timestamp = Column(DateTime, nullable=True)        # Fecha del mensaje
    rating = Column(Integer, nullable=True)            # Thumbs (-1, 0, 1)
    score = Column(Integer, nullable=True)             # Puntuación manual extendida
    tags = Column(JSON, nullable=True)                 # Etiquetas combinadas
    notes = Column(Text, nullable=True)                # Comentario del evaluador
    chat_title = Column(String, nullable=True)         # Título de la conversación
    feedback_id = Column(String, nullable=True)        # ID de evaluación
    usage = Column(JSON, nullable=True)                # Métricas técnicas (tokens, duración)
    chat_id = Column(String, nullable=True)            # ID de la conversación

    # 🔍 Métricas automáticas Opik (LLM-as-a-Judge)
    hallucination = Column(Float, nullable=True)
    moderation = Column(Float, nullable=True)
    context_precision = Column(Float, nullable=True)
    context_recall = Column(Float, nullable=True)
    usefulness = Column(Float, nullable=True)
    answer_relevance = Column(Float, nullable=True)
    g_eval = Column(Float, nullable=True)

    def __repr__(self):
        return f"<Interaction id={self.id} model={self.model}>"
