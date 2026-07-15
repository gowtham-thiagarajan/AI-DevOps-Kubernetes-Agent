from fastapi import APIRouter
from loguru import logger
from kubernetes.kubectl_executor import run_kubectl

router = APIRouter()


@router.get("/clusters")
async def list_clusters():
    """List kubeconfig contexts available on the host."""
    result = run_kubectl(["config", "get-contexts", "-o", "name"], timeout=10)
    if not result.get("success"):
        logger.error("Failed to list kube contexts: {}", result.get("stderr") or result.get("stdout"))
        return {"status": "error", "error": "Unable to list kubeconfig contexts", "details": result}

    contexts = [line.strip() for line in result.get("stdout", "").splitlines() if line.strip()]

    # also get current-context
    cur = run_kubectl(["config", "current-context"], timeout=5)
    current = cur.get("stdout", "").strip() if cur.get("success") else None

    return {"status": "success", "contexts": contexts, "current": current}
