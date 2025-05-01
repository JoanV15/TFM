# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

# Necesario para evitar errores en SQLite cuando múltiples hilos acceden a la base
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,  # <-- Uso de settings
    connect_args={"check_same_thread": False}
)

# Crea una clase "Session" para comunicarnos con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base a partir de la cual heredan todos los modelos (tablas)
Base = declarative_base()
