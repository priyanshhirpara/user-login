from database import Base
from sqlalchemy import Integer, String, Column, Date
from sqlalchemy.orm import relationship
from enum import Enum


class UserType(Enum):
    ADMIN = "admin"
    STUDENT = "student"
    TEACHER = "teacher"


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    username = Column(String, unique=True)
    email = Column(String)
    password = Column(String)
    birthdate = Column(Date)
    entries = relationship("Entry", back_populates="crater", uselist=True)
    user_type = Column(String, default=UserType.STUDENT.value, nullable=False)
    entries1 = relationship("Competition", back_populates="entries1", uselist=True)


user_curd = User
