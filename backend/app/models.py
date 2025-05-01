from sqlalchemy import Column, String, Text, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import JSON

Base = declarative_base()

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(String, primary_key=True, index=True)  # UUID del mensaje
    parent_id = Column(String, nullable=True)  # ID del padre (si existe)
    role = Column(String, nullable=False)  # 'user' o 'assistant'
    content = Column(Text, nullable=False)  # Texto del prompt o respuesta
    model = Column(String, nullable=True)  # Nombre del modelo usado
    timestamp = Column(DateTime, nullable=True)  # Timestamp UNIX
    rating = Column(Integer, nullable=True)  # Rating manual (-1, 0, 1)
    tags = Column(JSON, nullable=True)  # Lista de etiquetas
    feedback_id = Column(String, nullable=True)  # ID de feedback si existe

    def __repr__(self):
        return f"<Interaction id={self.id} role={self.role} model={self.model}>"
