from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship


class Entry(Base):
    __tablename__ = "Entry"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    title = Column(String)
    description = Column(String)
    submission_date = Column(Date)
    user_id = Column(Integer, ForeignKey("User.id"))
    competition_id = Column(Integer, ForeignKey("Competition.id"))
    crater = relationship("User", back_populates="entries")
    competition = relationship("Competition", back_populates="entries")
