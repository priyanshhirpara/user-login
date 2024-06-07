from fastapi import FastAPI
from database import engine
from src.user import api as user_api
from src.competition import api as competion_api
from src.entry import api as entry_api
from src.user.model import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_api.Router)
app.include_router(competion_api.Router)
app.include_router(entry_api.Router)
