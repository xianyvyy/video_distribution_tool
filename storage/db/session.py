"""
SQLAlchemy session and engine. Uses config.base.DATABASE_URL.
"""
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Lazy init to avoid import cycle
_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        try:
            from config.base import DATABASE_URL, DB_ECHO
        except ImportError:
            from video_distribution_tool.config.base import DATABASE_URL, DB_ECHO
        from .models import Base
        _engine = create_engine(DATABASE_URL, echo=DB_ECHO)
        Base.metadata.create_all(_engine)
    return _engine


def get_session_factory():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal


def get_session() -> Generator[Session, None, None]:
    """Dependency-style session; commit/rollback is caller's responsibility."""
    SessionLocal = get_session_factory()
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    """Create tables if not exist."""
    get_engine()
