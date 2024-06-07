# src/user/api.py

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from src.user import model, schemas
from passlib.context import CryptContext
from src.user.token import create_access_token, create_refresh_token
import bcrypt

Router = APIRouter(tags=["User"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@Router.post("/register")
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    existing_email = (
        db.query(model.User).filter(model.User.email == request.email).first()
    )
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        )

    existing_username = (
        db.query(model.User).filter(model.User.username == request.username).first()
    )
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
        )

    hashed_password = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt())
    user = model.User(
        firstname=request.firstname,
        lastname=request.lastname,
        username=request.username,
        email=request.email,
        password=hashed_password.decode(),
        birthdate=request.birthdate,  # Corrected column name
        user_type=request.user_type.value,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"email": user.email, "User": user.username}


@Router.post("/login")
def verify_user(request: schemas.Login, db: Session = Depends(get_db)):
    email = request.email
    password = request.password
    user = db.query(model.User).filter(model.User.email == email).first()
    if user and pwd_context.verify(password, user.password):
        access_token = create_access_token(
            {
                "sub": user.email,
                "id": user.id,
                "username": user.username,
                "user_type": user.user_type,
            }
        )
        refresh_token = create_refresh_token(
            {
                "sub": user.email,
                "id": user.id,
                "username": user.username,
                "user_type": user.user_type,
            }
        )

        return {
            "name": user.firstname + " " + user.lastname,
            "email": user.email,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer",
        }
    else:
        raise HTTPException(status_code=401, detail="Incorrect email or passwords")


@Router.get("/show/{id}", response_model=schemas.ShowUser)
def show_user(id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="This user is not exists"
        )
    return user
