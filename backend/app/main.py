from fastapi import FastAPI, Depends
from . import models, schemas, crud, lamb_api
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "FastApi Funcionando!"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/interactions/")
def read_interactions(db: Session = Depends(get_db)):
    return crud.get_interactions(db)

@app.post("/interactions/")
def create_interaction(interaction: schemas.InteractionCreate, db: Session = Depends(get_db)):
    return crud.create_interaction(db, interaction)

@app.post("/lamb_predict/")
def predict(prompt: str):
    return lamb_api.query_lamb_v4(prompt)
