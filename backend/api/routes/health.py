from fastapi import APIRouter

from models.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="healthy", service="ai-kubernetes-agent")
