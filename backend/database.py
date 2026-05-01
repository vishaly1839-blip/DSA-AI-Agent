"""
DSA AI Tutor Agent - Database Models
PostgreSQL database models
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), unique=True, index=True)
    username = Column(String(100))
    email = Column(String(100))
    password_hash = Column(String(255))
    level = Column(String(20), default="Beginner")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Progress(Base):
    """User progress model"""
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), index=True)
    topic = Column(String(50))
    attempts = Column(Integer, default=0)
    correct = Column(Integer, default=0)
    wrong = Column(Integer, default=0)
    time_spent = Column(Integer, default=0)  # seconds
    last_attempted = Column(DateTime, default=datetime.utcnow)


class Mistake(Base):
    """Mistake history model"""
    __tablename__ = "mistakes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), index=True)
    topic = Column(String(50))
    problem = Column(String(100))
    error_type = Column(String(50))
    description = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)


class Session(Base):
    """User session model"""
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), index=True)
    session_id = Column(String(100), unique=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    topics_covered = Column(JSON, default=list)
    messages_count = Column(Integer, default=0)


def init_db(database_url: str):
    """Initialize database"""
    from sqlalchemy import create_engine
    
    engine = create_engine(database_url)
    Base.metadata.create_all(bind=engine)
    return engine


def get_database_url():
    """Get database URL from environment"""
    import os
    
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "5432")
    name = os.environ.get("DB_NAME", "dsa_ai_tutor")
    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASSWORD", "postgres")
    
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


__all__ = ['User', 'Progress', 'Mistake', 'Session', 'init_db', 'get_database_url']
