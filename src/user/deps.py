from typing import Annotated, Tuple, Optional

import jwt
from fastapi import Depends, HTTPException, Header, Request, status
from sqlalchemy.orm import Session
from src.user.token import SECRET_KEY, ALGORITHM
from database import get_db
from src.user.model import User, UserType


def authenticated(request: Request):
    try:
        access_token = request.headers.get("Authorization")
        jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")


def _authenticated_user(
    authorization: str = Header(), db: Session = Depends(get_db)
) -> Tuple[User, Session]:
    try:
        access_token = authorization
        user = None
        if access_token:
            payload = jwt.decode(
                access_token.split()[1], SECRET_KEY, algorithms=ALGORITHM
            )
            user_id = payload["id"]
            if not user_id:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid User")
        else:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Authorization not found")
        return user, db
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")


# is_authorized = Annotated[bool, Depends(authenticated)]
authenticated_user = Annotated[Tuple[User, Session], Depends(_authenticated_user)]
