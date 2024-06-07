from typing import Tuple
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from src.competition import model, schemas
from passlib.context import CryptContext
from src.user.deps import authenticated_user
from src.competition.permission import teachers_admin
from src.user.model import User

Router = APIRouter(prefix="/competition", tags=["Competitions"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@Router.post("/")
def add_competition(
    request: schemas.Competition,
    user_db: Tuple[User, Session] = Depends(teachers_admin),
):
    user, db = user_db

    competition = model.Competition(**request.model_dump(), userid=user.id)
    db.add(competition)
    db.commit()
    db.refresh(competition)
    return competition


@Router.get("/")
def get_all(request: schemas.Competition, db: Session = Depends(get_db)):
    games = db.query(model.Competition).all()
    return games


@Router.get("/{id:int}")
def selected_competition(
    id: int, request: schemas.Competition, db: Session = Depends(get_db)
):
    selected = db.query(model.Competition).filter(model.Competition.id == id).first()
    if not selected:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Competition has not found"
        )
    return selected


@Router.put("/{id:int}")
def update(id: int, request: schemas.Competition, db: Session = Depends(get_db)):
    selected = db.query(model.Competition).filter(model.Competition.id == id).first()
    for key, value in request.model_dump().items():
        setattr(selected, key, value)
    if not selected:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Competition has not found"
        )
    db.commit()
    return "Update"


@Router.delete("/{id}")
def destroy(id: int, db: Session = Depends(get_db)):
    delete = (
        db.query(model.Competition)
        .filter(model.Competition.id == id)
        .delete(synchronize_session=False)
    )
    if not delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Competition has not found"
        )
    db.commit()
    return "Done"
