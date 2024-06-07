from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from src.entry import model, schemas
from src.competition.model import Competition
from src.competition.permission import student_admin
from src.user.model import User
from typing import Tuple


Router = APIRouter(prefix="/entry", tags=["Competition entry"])


@Router.post("/")
def entry(
    request: schemas.Entry, user_db: Tuple[User, Session] = Depends(student_admin)
):
    user, db = user_db
    comp = (
        db.query(Competition).filter(Competition.id == request.competition_id).first()
    )
    # breakpoint()
    if comp.start_date > request.submission_date:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This competition is not started",
        )

    if comp.end_date < request.submission_date:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This competition is over"
        )
    entry = model.Entry(
        name=request.name,
        title=request.title,
        description=request.description,
        submission_date=request.submission_date,
        user_id=user.id,
        competition_id=request.competition_id,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@Router.get("/")
def get_all(request: schemas.Entry, db: Session = Depends(get_db)):
    entry = db.query(model.Entry).all()
    return entry


@Router.get("/{id}")
def selected_entry(id: int, request: schemas.Entry, db: Session = Depends(get_db)):
    selected_entry1 = db.query(model.Entry).filter(model.Entry.id == id).first()
    if not selected_entry1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Entry has not found"
        )
    return selected_entry1


@Router.put("/{id}")
def update(id: int, request: schemas.Entry, db: Session = Depends(get_db)):
    update = db.query(model.Entry).filter(model.Entry.id == id).first()
    for key, value in request.model_dump().items():
        setattr(update, key, value)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Entry has not found"
        )
    db.commit()
    return "Update"


@Router.delete("/{id}")
def destroy(id: int, request: schemas.Entry, db: Session = Depends(get_db)):
    delete = db.query(model.Entry).filter(model.Entry.id == id).first()
    if not delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Entry has not found"
        )
    db.commit()
    return "done"
