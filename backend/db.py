import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import settings

DATABASE_URL = settings.database_url or os.getenv("DATABASE_URL") or "sqlite:///./ai_kubernetes_agent.db"

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
Base = declarative_base()


def init_db() -> None:
    """Create database tables if they do not already exist."""
    from models.entities import Base as EntitiesBase

    EntitiesBase.metadata.create_all(bind=engine)
