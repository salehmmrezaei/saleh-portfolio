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



class Experience(Base):
    __tablename__ = "experience"
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, index=True)
    role = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    skills = Column(ARRAY(String), default=[])
    url = Column(String)
    description = Column(ARRAY(String), default=[])

class Education(Base):
    __tablename__ = "education"
    id = Column(Integer, primary_key=True, index=True)
    institution = Column(String, index=True)
    degree = Column(String)
    grade = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    country = Column(String)