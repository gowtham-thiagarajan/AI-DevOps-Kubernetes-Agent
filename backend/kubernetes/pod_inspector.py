import json
from typing import Any

from loguru import logger

from .kubectl_executor import run_kubectl

PROBLEM_STATUSES = {
    "CrashLoopBackOff",
    "ImagePullBackOff",
    "Pending",
    "Error",
    "OOMKilled",
    "ContainerCreating",
}


def _pod_status_from_item(item: dict[str, Any]) -> str:
    status = item.get("status", {})
    pod_phase = status.get("phase", "")
    pod_reason = status.get("reason") or ""

    if pod_reason:
        return pod_reason

    for container in status.get("containerStatuses", []) or []:
        state = container.get("state", {})
        waiting = state.get("waiting")
        terminated = state.get("terminated")
        if waiting and waiting.get("reason"):
            return waiting["reason"]
        if terminated and terminated.get("reason"):
            return terminated["reason"]
        if waiting:
            return "ContainerCreating"

    return pod_phase or "Unknown"


def _is_problematic_status(status: str) -> bool:
    normalized = status.strip()
    if not normalized:
        return False
    if normalized in PROBLEM_STATUSES:
        return True
    for problem in PROBLEM_STATUSES:
        if problem.lower() in normalized.lower():
            return True
    return False


def inspect_pods() -> dict[str, Any]:
    result = run_kubectl(["get", "pods", "-A", "-o", "json"])
    if not result["success"]:
        return {
            "healthy": False,
            "total_pods": 0,
            "problematic_pods": [],
            "error": result["stderr"] or result["stdout"],
        }

    try:
        payload = json.loads(result["stdout"])
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse pod JSON: {}", exc)
        return {
            "healthy": False,
            "total_pods": 0,
            "problematic_pods": [],
            "error": "Failed to parse kubectl pod output.",
        }

    items = payload.get("items", [])
    problematic_pods: list[dict[str, Any]] = []

    for item in items:
        metadata = item.get("metadata", {})
        name = metadata.get("name", "unknown")
        namespace = metadata.get("namespace", "default")
        status = _pod_status_from_item(item)

        if _is_problematic_status(status):
            problematic_pods.append(
                {
                    "name": name,
                    "namespace": namespace,
                    "status": status,
                }
            )

    return {
        "healthy": len(problematic_pods) == 0,
        "total_pods": len(items),
        "problematic_pods": problematic_pods,
    }
