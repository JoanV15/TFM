# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Conexión a base de datos local SQLite (webui.db debe estar en la raíz del proyecto)
SQLALCHEMY_DATABASE_URL = "sqlite:///./webui.db"

# Necesario para evitar errores en SQLite cuando múltiples hilos acceden a la base
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crea una clase "Session" para comunicarnos con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base a partir de la cual heredan todos los modelos (tablas)
Base = declarative_base()
