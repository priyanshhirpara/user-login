from typing import Tuple
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.user.deps import authenticated_user
from src.user.model import User


def teachers_admin(user_db: authenticated_user) -> Tuple[User, Session]:
    user, db = user_db
    if user.user_type == "student":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Permission Denied")
    return user, db


def student_admin(user_db: authenticated_user) -> Tuple[User, Session]:
    user, db = user_db
    if user.user_type == "teacher":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Permission Denied")
    return user, db


def admin_auth(user_db: authenticated_user) -> Tuple[User, Session]:
    user, db = user_db
    if user.user_type != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Permission Denied")
    return user, db


def teachers_auth(user_db: authenticated_user) -> Tuple[User, Session]:
    user, db = user_db
    if user.user_type != "teacher":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Permission Denied")
    return user, db


def student_auth(user_db: authenticated_user) -> Tuple[User, Session]:
    user, db = user_db
    if user.user_type != "student":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Permission Denied")
    return user, db
