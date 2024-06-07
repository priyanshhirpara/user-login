from pydantic import BaseModel
from datetime import date


class Entry(BaseModel):
    name: str
    title: str
    description: str
    submission_date: date
    competition_id: int

    class Config:
        from_attributes = True
