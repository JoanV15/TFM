from fastapi import FastAPI, Depends, Query, HTTPException
from . import models, schemas, crud, lamb_api, sync_utils
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from .schemas import InteractionOut
from sqlalchemy import func
from app.schemas import EvaluationUpdate
from app.models import Interaction
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Backend TFM",
    version="1.0.0",
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Sistema"])
async def root():
    return {"message": "FastApi Funcionando!"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/interactions", response_model=List[InteractionOut], tags=["Interacciones"])
def read_interactions(
    role: Optional[str] = Query(None, description="Filtrar por role ('user' o 'assistant')"),
    rating: Optional[int] = Query(None, description="Filtrar por rating (-1, 0, 1)"),
    model: Optional[str] = Query(None, description="Filtrar por modelo usado"),
    tag: Optional[str] = Query(None, description="Filtrar si el tag existe"),
    limit: int = Query(20, description="Número máximo de resultados a devolver"),
    offset: int = Query(0, description="Desplazamiento desde el inicio de los resultados"),
    db: Session = Depends(get_db),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    if role == "user" and rating is not None:
        raise HTTPException(status_code=400, detail="No se puede filtrar por rating cuando role es 'user'")

    return crud.get_filtered_interactions(
    db, role=role, rating=rating, model=model, tag=tag,
    limit=limit, offset=offset,
    date_from=date_from, date_to=date_to, search=search)

@app.get("/interactions/{interaction_id}", response_model=InteractionOut, tags=["Interacciones"])
def get_interaction(interaction_id: str, db: Session = Depends(get_db)):
    interaction = crud.get_interaction_by_id(db, interaction_id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interacción no encontrada")
    return interaction

@app.post("/interactions", tags=["Interacciones"])
def create_interaction(interaction: schemas.InteractionCreate, db: Session = Depends(get_db)):
    return crud.create_interaction(db, interaction)

@app.post("/sync_webui_db", tags=["Sincronización"])
def sync_webui_db():
    return sync_utils.sync_latest_chats()

@app.get("/stats", tags=["Estadísticas"])
def get_stats(db: Session = Depends(get_db)) -> Dict[str, Any]:
    total = db.query(func.count(models.Interaction.id)).scalar()
    total_user = db.query(func.count(models.Interaction.id)).filter(models.Interaction.role == "user").scalar()
    total_assistant = db.query(func.count(models.Interaction.id)).filter(models.Interaction.role == "assistant").scalar()
    rated_positive = db.query(func.count(models.Interaction.id)).filter(models.Interaction.rating == 1).scalar()
    rated_negative = db.query(func.count(models.Interaction.id)).filter(models.Interaction.rating == -1).scalar()
    rated_neutral = db.query(func.count(models.Interaction.id)).filter((models.Interaction.rating == 0) | (models.Interaction.rating == None)).scalar()

    results = db.query(Interaction.model, func.count(Interaction.model)).group_by(Interaction.model).all()
    model_counts = {model: count for model, count in results}

    tags_counter = {}
    interactions = db.query(models.Interaction.tags).filter(models.Interaction.tags.isnot(None)).all()
    for (tags,) in interactions:
        if tags:
            for tag in tags:
                tags_counter[tag] = tags_counter.get(tag, 0) + 1

    return {
        "total_interactions": total,
        "total_user_messages": total_user,
        "total_assistant_messages": total_assistant,
        "rated_positive": rated_positive,
        "rated_negative": rated_negative,
        "rated_neutral": rated_neutral,
        "models_usage": model_counts,
        "tags_usage": tags_counter
    }

@app.post("/evaluation/{interaction_id}")
def update_evaluation(interaction_id: int, eval_data: EvaluationUpdate, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")

    if eval_data.score is not None:
        interaction.score = eval_data.score
    if eval_data.notes is not None:
        interaction.notes = eval_data.notes
    if eval_data.tags is not None:
        interaction.tags = eval_data.tags # type: ignore

    db.commit()
    return {"message": "Evaluation updated successfully"}
    
#@app.post("/lamb_predict/", tags=["Lamb API"])
#def predict(prompt: str):
#    return lamb_api.query_lamb_v4(prompt)