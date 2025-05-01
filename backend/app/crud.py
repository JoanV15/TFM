from sqlalchemy.orm import Session
from .models import Interaction
from .schemas import InteractionCreate
from sqlalchemy import and_
from datetime import datetime

def create_interaction(db: Session, interaction: InteractionCreate):
    db_inter = Interaction(**interaction.dict())
    db.add(db_inter)
    db.commit()
    db.refresh(db_inter)
    return db_inter

def get_filtered_interactions(db: Session, role=None, rating=None, model=None, tag=None, limit=20, offset=0, date_from=None, date_to=None, search=None):
    query = db.query(Interaction)

    if role:
        query = query.filter(Interaction.role == role)
    if rating is not None:
        query = query.filter(Interaction.rating == rating)
    if model:
        query = query.filter(Interaction.model == model)
    if tag:
        query = query.filter(Interaction.tags.contains([tag]))
    if date_from:
        from_date = datetime.strptime(date_from, "%Y-%m-%d")
        query = query.filter(Interaction.timestamp >= from_date)
    if date_to:
        to_date = datetime.strptime(date_to, "%Y-%m-%d")
        query = query.filter(Interaction.timestamp <= to_date)
    if search:
        query = query.filter(
            Interaction.content.ilike(f"%{search}%")
    )

    return query.offset(offset).limit(limit).all()


def get_interaction_by_id(db: Session, interaction_id: str):
    return db.query(Interaction).filter(Interaction.id == interaction_id).first()