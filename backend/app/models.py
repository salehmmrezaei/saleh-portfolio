from typing import List
from sqlalchemy import Column, Integer, String
from .database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    skills = Column(List(String), default=[])
    url = Column(String)
    description = Column(List(String), default=[])