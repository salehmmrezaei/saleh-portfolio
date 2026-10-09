from sqlalchemy import (
    Boolean,
    Column,
    Computed,
    Date,
    DateTime,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, TSVECTOR
from pgvector.sqlalchemy import VECTOR
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


class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"
    __table_args__ = (
        UniqueConstraint(
            "source_type",
            "source_key",
            "section",
            "chunk_index",
            name="uq_knowledge_chunk_identity",
        ),
    )

    id = Column(Integer, primary_key=True)
    source_type = Column(String(32), nullable=False, index=True)
    source_key = Column(String(128), nullable=False, index=True)
    section = Column(String(64), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    content_hash = Column(String(64), nullable=False)

    embedding_model = Column(String(100), nullable=True)
    embedding = Column(VECTOR(1536), nullable=True)

    search_document = Column(
        TSVECTOR,
        Computed(
            "to_tsvector("
            "'english'::regconfig, "
            "coalesce(title, '') || ' ' || content"
            ")",
            persisted=True,
        ),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
