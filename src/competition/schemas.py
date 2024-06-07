from pydantic import BaseModel
from datetime import date


class Competition(BaseModel):
    name: str
    description: str
    start_date: date
    end_date: date
    prize: bool

    class Config:
        from_attributes = True
