from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from db import Base


class Investigation(Base):
    __tablename__ = "investigations"

    id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    root_cause = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)
    confidence = Column(Integer, nullable=False)
    namespace = Column(String, nullable=False, default="default")
    status = Column(String, nullable=False, default="success")

    progress = relationship("InvestigationProgress", back_populates="investigation")


class InvestigationProgress(Base):
    __tablename__ = "investigation_progress"

    id = Column(Integer, primary_key=True, index=True)
    investigation_id = Column(String, ForeignKey("investigations.id"), nullable=False)
    step = Column(String, nullable=False)
    detail = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="completed")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    investigation = relationship("Investigation", back_populates="progress")
