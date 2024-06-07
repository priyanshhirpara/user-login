import jwt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Header
from datetime import datetime, timedelta
from database import get_db
from src.user import model

SECRET_KEY = "0a4811b627a0f8e060eab5e1a8c8579aa7bb356a"
ALGORITHM = "HS256"
ACCESS_TOKEN = 120
REFRESH_TOKEN = 60


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=REFRESH_TOKEN)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# def decode_token(authorization: str = Header(), db: Session = Depends(get_db)):
#     try:
#         parts = authorization.split(" ")
#         verify = parts[1]
#         payload = jwt.decode(verify, SECRET_KEY, algorithms=ALGORITHM)
#         email_ext = payload.get("sub")
#         user_ext = db.query(model.User).filter(model.User.email == email_ext).first()
#         if not email_ext:
#             raise HTTPException(status_code=400, detail="Email is not found token")
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token has expired")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="Invalid token")


# def refresh_token(refresh_token: str = Header(), db: Session = Depends(get_db)):
#     try:
#         payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=ALGORITHM)
#         email = payload.get("sub")
#         user = db.query(model.USer).filter(model.User.email == email).first()
#         if user:
#             access_token = create_access_token(user)
#             return {"access_token": access_token}
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Refresh token has expired")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="Invalid Refresh token")
