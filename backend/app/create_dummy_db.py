from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///../data/webui.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text)
    response = Column(Text)
    thumbs = Column(String)  # "up", "down", or None

Base.metadata.create_all(bind=engine)

print("Base de datos webui.db creada con tabla 'interactions'")

