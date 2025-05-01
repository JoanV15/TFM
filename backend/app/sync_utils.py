import sqlite3
import json
import logging
from sqlalchemy.orm import Session
from .models import Interaction
from .database import SessionLocal
from .config import settings
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def parse_timestamp(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, int):
        try:
            return datetime.fromtimestamp(value)
        except Exception:
            return None
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except Exception:
            return None
    return None

def sync_latest_chats():
    try:
        conn = sqlite3.connect(settings.OPENWEBUI_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, chat FROM chat ORDER BY created_at DESC")
        chats = cursor.fetchall()
    except Exception as e:
        logging.error(f"Error al leer webui.db: {e}")
        return {"status": "error", "message": str(e)}

    db: Session = SessionLocal()
    imported = 0

    # Recuperar todos los IDs ya almacenados
    existing_ids = {row[0] for row in db.query(Interaction.id).all()}

    for chat_id, chat_json_raw in chats:
        try:
            parsed_chat = json.loads(chat_json_raw)
            messages = parsed_chat.get("history", {}).get("messages", {})

            for msg_id, msg in messages.items():
                if msg_id in existing_ids:
                    continue  # Ya existe, saltamos

                raw_tags = msg.get("annotation", {}).get("tags")
                if isinstance(raw_tags, list) and len(raw_tags) > 0 and isinstance(raw_tags[0], list):
                    tags = raw_tags[0]
                else:
                    tags = raw_tags

                interaction = Interaction(
                    id=msg_id,
                    parent_id=msg.get("parentId"),
                    role=msg.get("role"),
                    content=msg.get("content"),
                    model=msg.get("model"),
                    timestamp=parse_timestamp(msg.get("timestamp")),
                    rating=msg.get("annotation", {}).get("rating"),
                    tags=tags,
                    feedback_id=msg.get("feedbackId")
                )
                db.add(interaction)
                imported += 1
        except Exception as e:
            logging.warning(f"Chat {chat_id} falló: {e}")
            continue

    db.commit()
    db.close()
    return {"status": "success", "imported": imported}