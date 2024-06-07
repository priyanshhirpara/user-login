from database import Base
from sqlalchemy import Column, String, Boolean, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Competition(Base):
    __tablename__ = "Competition"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    prize = Column(Boolean)
    userid = Column(Integer, ForeignKey("User.id"))
    entries1 = relationship("User", back_populates="entries1")
    entries = relationship("Entry", back_populates="competition", uselist=True)
