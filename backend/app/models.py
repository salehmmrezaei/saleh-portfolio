from sqlalchemy import Boolean, Column, Date, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from .database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    skills = Column(ARRAY(String), default=list, nullable=False)
    url = Column(String, nullable=False)
    description = Column(ARRAY(String), default=list, nullable=False)



class Experience(Base):
    __tablename__ = "experience"
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, index=True, nullable=False)
    company_slug = Column(String, index=True, nullable=False, unique=True)
    role = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    skills = Column(ARRAY(String), default=list, nullable=False)
    url = Column(String, nullable=False)
    description = Column(ARRAY(String), default=list, nullable=False)

class Education(Base):
    __tablename__ = "education"
    id = Column(Integer, primary_key=True, index=True)
    institution = Column(String, index=True, nullable=False)
    degree = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    country = Column(String, nullable=False)

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    skills = Column(ARRAY(String), default=list, nullable=False)
    description = Column(String, nullable=False)
    featured = Column(Boolean, default=False, nullable=False)