"""
Investigation history storage and retrieval.
Uses SQLAlchemy to persist investigation records and progress events.
"""
import uuid
from typing import List
from db import SessionLocal
from models.entities import Investigation, InvestigationProgress


def _investigation_to_dict(investigation: Investigation) -> dict:
    return {
        "id": investigation.id,
        "timestamp": investigation.timestamp.isoformat(),
        "root_cause": investigation.root_cause,
        "explanation": investigation.explanation,
        "confidence": investigation.confidence,
        "namespace": investigation.namespace,
        "status": investigation.status,
    }


def save_investigation(
    root_cause: str,
    explanation: str,
    confidence: int,
    namespace: str = "default",
    status: str = "success",
) -> dict:
    """Save investigation result to history."""
    investigation_id = f"inv_{uuid.uuid4().hex}"
    with SessionLocal() as session:
        investigation = Investigation(
            id=investigation_id,
            root_cause=root_cause,
            explanation=explanation,
            confidence=confidence,
            namespace=namespace,
            status=status,
        )
        session.add(investigation)
        session.commit()
        session.refresh(investigation)
        return _investigation_to_dict(investigation)


def save_investigation_progress(
    investigation_id: str,
    step: str,
    detail: str | None = None,
    status: str = "completed",
) -> dict:
    """Save investigation progress detail."""
    with SessionLocal() as session:
        record = InvestigationProgress(
            investigation_id=investigation_id,
            step=step,
            detail=detail,
            status=status,
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return {
            "id": record.id,
            "investigation_id": record.investigation_id,
            "step": record.step,
            "detail": record.detail,
            "status": record.status,
            "created_at": record.created_at.isoformat(),
        }


def get_investigations(limit: int = 10) -> List[dict]:
    """Get recent investigations."""
    with SessionLocal() as session:
        results = (
            session.query(Investigation)
            .order_by(Investigation.timestamp.desc())
            .limit(limit)
            .all()
        )
        return [_investigation_to_dict(inv) for inv in results]


def clear_history() -> None:
    """Clear all investigations (for testing)."""
    with SessionLocal() as session:
        session.query(InvestigationProgress).delete()
        session.query(Investigation).delete()
        session.commit()
