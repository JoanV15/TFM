import sqlite3
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Interaction

# --- CONFIGURACIÓN ---
# Ruta al archivo webui.db generado por OpenWebUI
WEBUI_DB_PATH = "../backend/webui.db"  # Ajusta si necesario
CHAT_ID = "9ed57334-9433-494a-99e1-034298acd27d"

# Ruta de tu base de datos consolidada (puede ser temporal inicialmente)
CONSOLIDATED_DB_PATH = "sqlite:///./interactions.db"

# --- CONEXIÓN A LA BASE CONSOLIDADA ---
engine = create_engine(CONSOLIDATED_DB_PATH)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)
session = SessionLocal()

# --- LECTURA DEL JSON DESDE webui.db ---
conn = sqlite3.connect(WEBUI_DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT chat FROM chat WHERE id = ?", (CHAT_ID,))
row = cursor.fetchone()

if not row:
    print("❌ No se encontró el chat especificado.")
    exit()

chat_json = json.loads(row[0])
messages = chat_json.get("history", {}).get("messages", {})

# --- PROCESAMIENTO E INSERCIÓN ---
for msg_id, msg in messages.items():
    interaction = Interaction(
        id=msg_id,
        parent_id=msg.get("parentId"),
        role=msg.get("role"),
        content=msg.get("content"),
        model=msg.get("model"),
        timestamp=msg.get("timestamp"),
        rating=msg.get("annotation", {}).get("rating"),
        tags=msg.get("annotation", {}).get("tags"),
        feedback_id=msg.get("feedbackId")
    )
    session.merge(interaction)

session.commit()
session.close()
print("✅ Datos importados correctamente a interactions.db")