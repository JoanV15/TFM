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
        cursor.execute("SELECT id, title, chat, meta FROM chat ORDER BY created_at DESC")
        chats = cursor.fetchall()
    except Exception as e:
        logging.error(f"Error al leer webui.db: {e}")
        return {"status": "error", "message": str(e)}

    db: Session = SessionLocal()
    imported = 0

    # IDs ya presentes en la base consolidada
    existing_ids = {row[0] for row in db.query(Interaction.id).all()}

    for chat_id, chat_title, chat_json_raw, meta_raw in chats:
        try:
            parsed_chat = json.loads(chat_json_raw)
            meta = json.loads(meta_raw) if meta_raw else {}
            global_tags = meta.get("tags", [])

            messages = parsed_chat.get("history", {}).get("messages", {})
            message_dict = {msg["id"]: msg for msg in messages.values()}

            for msg in messages.values():
                if msg.get("role") != "assistant":
                    continue

                msg_id = msg["id"]
                if msg_id in existing_ids:
                    continue

                parent_id = msg.get("parentId")
                parent_msg = messages.get(parent_id) if parent_id else None
                if not parent_msg or parent_msg.get("role") != "user":
                    continue

                # Tags combinadas
                raw_tags = msg.get("annotation", {}).get("tags")
                if isinstance(raw_tags, list) and len(raw_tags) > 0 and isinstance(raw_tags[0], list):
                    local_tags = raw_tags[0]
                else:
                    local_tags = raw_tags or []

                combined_tags = list(set(global_tags + local_tags))

                rating_val = msg.get("annotation", {}).get("rating")
                score = None  # score lo definirá el evaluador humano

                interaction = Interaction(
                    id=msg_id,
                    parent_id=parent_id,
                    prompt=parent_msg.get("content", ""),
                    response=msg.get("content", ""),
                    model=msg.get("model"),
                    timestamp=parse_timestamp(msg.get("timestamp")),
                    rating=rating_val,
                    score=score,
                    tags=combined_tags,
                    notes=None,
                    chat_title=chat_title,
                    feedback_id=msg.get("feedbackId"),
                    usage=msg.get("usage"),
                    chat_id=chat_id
                )
                db.add(interaction)
                imported += 1

        except Exception as e:
            logging.warning(f"Chat {chat_id} falló: {e}")
            continue

    db.commit()
    db.close()
    return {"status": "success", "imported": imported}
