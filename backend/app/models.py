from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from .database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    skills = Column(ARRAY(String), default=[])
    url = Column(String)
    description = Column(ARRAY(String), default=[])