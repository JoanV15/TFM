from sqlalchemy.orm import Session
from .models import Interaction
from .schemas import InteractionCreate, EvaluationUpdate
from sqlalchemy import and_, or_
from sqlalchemy import cast
from sqlalchemy.types import String
from datetime import datetime

def create_interaction(db: Session, interaction: InteractionCreate):
    db_inter = Interaction(**interaction.dict())
    db.add(db_inter)
    db.commit()
    db.refresh(db_inter)
    return db_inter

def get_filtered_interactions(db: Session, rating=None, model=None, score=None, tag=None, limit=20, offset=0, date_from=None, date_to=None, search=None):
    query = db.query(Interaction)

    if score == 'null':
        query = query.filter(Interaction.score == None)
    elif score is not None:
        query = query.filter(Interaction.score == score)
    if rating == 0:
        query = query.filter(or_(Interaction.rating == 0, Interaction.rating == None))
    elif rating is not None:
        query = query.filter(Interaction.rating == rating)
    if model:
        query = query.filter(Interaction.model == model)
    if tag:
        query = query.filter(cast(Interaction.tags, String).like(f'%"{tag}"%'))
    if date_from:
        from_date = datetime.strptime(date_from, "%Y-%m-%d")
        query = query.filter(Interaction.timestamp >= from_date)
    if date_to:
        to_date = datetime.strptime(date_to, "%Y-%m-%d")
        query = query.filter(Interaction.timestamp <= to_date)
    if search:
        query = query.filter(
            or_(
                Interaction.prompt.ilike(f"%{search}%"),
                Interaction.response.ilike(f"%{search}%"),
                Interaction.notes.ilike(f"%{search}%")
            )
        )

    return query.offset(offset).limit(limit).all()

def get_interaction_by_id(db: Session, interaction_id: str):
    return db.query(Interaction).filter(Interaction.id == interaction_id).first()

def update_evaluation(db: Session, interaction_id: str, evaluation: EvaluationUpdate):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        return None
    data = evaluation.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(interaction, key, value)
    db.commit()
    db.refresh(interaction)
    return interaction
