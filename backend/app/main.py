from fastapi import FastAPI, Depends, Query, HTTPException, Body
import os
from dotenv import load_dotenv
from . import models, schemas, crud, lamb_api, sync_utils
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any, Union
from .schemas import InteractionOut, InteractionCreate, EvaluationUpdate
from .models import Interaction
from sqlalchemy import func
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from datetime import datetime
import json
import csv

from opik.evaluation.metrics import (
    Equals, Contains, RegexMatch, IsJson, LevenshteinRatio,
    Hallucination, Moderation, ContextPrecision, ContextRecall,
    Usefulness, AnswerRelevance, GEval
)

# ======================
# Configuración básica
# ======================

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ======================
# Sistema
# ======================

@app.get("/", tags=["Sistema"])
async def root():
    return {"message": "FastApi Funcionando!"}

# ======================
# Sincronización
# ======================

@app.get("/stats", tags=["Estadísticas"])
def get_stats(db: Session = Depends(get_db)) -> Dict[str, Any]:
    total = db.query(func.count(models.Interaction.id)).scalar()
    rated_positive = db.query(func.count(models.Interaction.id)).filter(models.Interaction.rating == 1).scalar()
    rated_negative = db.query(func.count(models.Interaction.id)).filter(models.Interaction.rating == -1).scalar()
    rated_neutral = db.query(func.count(models.Interaction.id)).filter(
        (models.Interaction.rating == 0) | (models.Interaction.rating == None)
    ).scalar()

    results = db.query(models.Interaction.model, func.count(models.Interaction.model)).group_by(models.Interaction.model).all()
    model_counts = {model: count for model, count in results}

    tags_counter = {}
    interactions = db.query(models.Interaction.tags).filter(models.Interaction.tags.isnot(None)).all()
    for (tags,) in interactions:
        if tags:
            for tag in tags:
                tags_counter[tag] = tags_counter.get(tag, 0) + 1

    return {
        "total_interactions": total,
        "rated_positive": rated_positive,
        "rated_negative": rated_negative,
        "rated_neutral": rated_neutral,
        "models_usage": model_counts,
        "tags_usage": tags_counter
    }

@app.post("/sync_webui_db", tags=["Sincronización"])
def sync_webui_db():
    return sync_utils.sync_latest_chats()

# ======================
# Interacciones
# ======================

@app.get("/interactions", response_model=List[InteractionOut], tags=["Interacciones"])
def read_interactions(
    model: Optional[str] = Query(None),
    score: Optional[Union[int, str]] = Query(None),
    rating: Optional[int] = Query(None),
    tag: Optional[str] = Query(None),
    limit: int = Query(20),
    offset: int = Query(0),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return crud.get_filtered_interactions(
        db, model=model, rating=rating, score=score, tag=tag,
        limit=limit, offset=offset,
        date_from=date_from, date_to=date_to, search=search
    )

@app.get("/interactions/{interaction_id}", response_model=InteractionOut, tags=["Interacciones"])
def get_interaction(interaction_id: str, db: Session = Depends(get_db)):
    interaction = crud.get_interaction_by_id(db, interaction_id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interacción no encontrada")
    return interaction

@app.post("/interactions", response_model=InteractionOut, tags=["Interacciones"])
def create_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
    return crud.create_interaction(db, interaction)

# ======================
# Evaluación manual
# ======================

@app.post("/evaluation/{interaction_id}", tags=["Evaluación manual"])
def update_evaluation(interaction_id: str, eval_data: EvaluationUpdate, db: Session = Depends(get_db)):
    interaction = crud.update_evaluation(db, interaction_id, eval_data)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return {"message": "Evaluation updated successfully"}

# ======================
# Evaluación automática
# ======================

@app.post("/opik/evaluate/{interaction_id}", tags=["Evaluación automática"])
def evaluate_with_opik(interaction_id: str, db: Session = Depends(get_db)):
    interaction = crud.get_interaction_by_id(db, interaction_id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interacción no encontrada")

    prompt: str = interaction.prompt  # type: ignore
    response: str = interaction.response  # type: ignore
    expected: str = interaction.response  # type: ignore
    context = [""]

    try:
        model = OPENAI_MODEL

        interaction.hallucination = Hallucination(model=model).score(input=prompt, output=response).value  # type: ignore
        interaction.moderation = Moderation(model=model).score(input=prompt, output=response).value  # type: ignore

        interaction.context_precision = ContextPrecision(model=model).score( # type: ignore
            input=prompt, output=response, expected_output=expected, context=context
        ).value  # type: ignore

        interaction.context_recall = ContextRecall(model=model).score( # type: ignore
            input=prompt, output=response, expected_output=expected, context=context
        ).value  # type: ignore

        interaction.usefulness = Usefulness(model=model).score(input=prompt, output=response).value  # type: ignore

        interaction.answer_relevance = AnswerRelevance(model=model, require_context=False).score( # type: ignore
            input=prompt, output=response
        ).value  # type: ignore

        interaction.g_eval = GEval( # type: ignore
            task_introduction="Evalúa la calidad de la respuesta en base a su claridad y validez.",
            evaluation_criteria="La respuesta está bien explicada y es correcta.",
            model=model
        ).score(input=prompt, output=response).value  # type: ignore

        db.commit()

        return {
            "message": "Métricas evaluadas y guardadas con éxito",
            "metrics": {
                "hallucination": interaction.hallucination,
                "moderation": interaction.moderation,
                "context_precision": interaction.context_precision,
                "context_recall": interaction.context_recall,
                "usefulness": interaction.usefulness,
                "answer_relevance": interaction.answer_relevance,
                "g_eval": interaction.g_eval
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al evaluar métricas automáticas: {str(e)}")

# ======================
# Métricas heurísticas
# ======================

@app.post("/metrics/heuristics", tags=["Métricas heurísticas"])
def compute_heuristic_metrics(
    expected_output: str = Body(...),
    actual_output: str = Body(...)
):
    try:
        return {
            "equals": Equals().score(expected_output, actual_output).value,
            "contains": Contains().score(expected_output, actual_output),
            "regexmatch": RegexMatch(regex=expected_output).score(actual_output),
            "isjson": IsJson().score(actual_output).value,
            "levenshtein": LevenshteinRatio().score(expected_output, actual_output).value
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al calcular métricas heurísticas: {str(e)}")

# ======================
# Exportación
# ======================

@app.get("/export_interactions", tags=["Exportación"])
def export_interactions(db: Session = Depends(get_db)):
    file_path = "interactions_export.json"
    all_interactions = db.query(models.Interaction).all()

    export_data = []
    exported_ids = []
    skipped_count = 0

    for i in all_interactions:
        if i.score is not None:
            export_data.append({
                "input": i.prompt,
                "expected_output": i.response,
                "score": i.score,
                "rating": i.rating,
                "model": i.model,
                "timestamp": i.timestamp.isoformat() if isinstance(i.timestamp, datetime) else "",
                "tags": i.tags if isinstance(i.tags, list) else [],
                # Nuevas métricas automáticas de Opik
                "hallucination": i.hallucination,
                "moderation": i.moderation,
                "context_precision": i.context_precision,
                "context_recall": i.context_recall,
                "usefulness": i.usefulness,
                "answer_relevance": i.answer_relevance,
                "g_eval": i.g_eval
            })
            exported_ids.append(i.id)
        else:
            skipped_count += 1

    with open(file_path, "w", encoding="utf-8") as jsonfile:
        json.dump(export_data, jsonfile, ensure_ascii=False, indent=2)

    return {
        "file": file_path,
        "evaluated_ids": exported_ids,
        "skipped_count": skipped_count
    }
