from sqlalchemy.orm import Session
from .models import Interaction
from .schemas import InteractionCreate

def get_interactions(db: Session, thumbs_filter=None):
    query = db.query(Interaction)
    if thumbs_filter:
        query = query.filter(Interaction.thumbs == thumbs_filter)
    return query.all()

def create_interaction(db: Session, interaction: InteractionCreate):
    db_inter = Interaction(**interaction.dict())
    db.add(db_inter)
    db.commit()
    db.refresh(db_inter)
    return db_inter
