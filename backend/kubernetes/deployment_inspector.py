import json
from typing import Any

from loguru import logger

from .kubectl_executor import run_kubectl


def _deployment_status(deployment: dict[str, Any]) -> bool:
    desired = deployment.get("desired_replicas", 0)
    available = deployment.get("available_replicas", 0)
    unavailable = deployment.get("unavailable_replicas", 0)
    conditions = deployment.get("conditions", []) or []

    if available < desired:
        return False
    if unavailable > 0:
        return False

    for condition in conditions:
        if condition.get("type") == "Available" and condition.get("status") != "True":
            return False
        if condition.get("type") == "Progressing" and condition.get("status") != "True":
            return False

    return True


def inspect_deployments() -> dict[str, Any]:
    result = run_kubectl(["get", "deployments", "-A", "-o", "json"])
    if not result["success"]:
        return {
            "healthy": False,
            "total_deployments": 0,
            "unhealthy_deployments": [],
            "error": result["stderr"] or result["stdout"],
        }

    try:
        payload = json.loads(result["stdout"])
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse deployment JSON: {}", exc)
        return {
            "healthy": False,
            "total_deployments": 0,
            "unhealthy_deployments": [],
            "error": "Failed to parse kubectl deployment output.",
        }

    items = payload.get("items", [])
    unhealthy_deployments: list[dict[str, Any]] = []

    for item in items:
        metadata = item.get("metadata", {})
        status = item.get("status", {})
        name = metadata.get("name", "unknown")
        namespace = metadata.get("namespace", "default")
        desired = status.get("replicas", 0)
        available = status.get("availableReplicas", 0)
        unavailable = status.get("unavailableReplicas", 0)
        conditions = status.get("conditions", []) or []

        deployment = {
            "name": name,
            "namespace": namespace,
            "desired_replicas": desired,
            "available_replicas": available,
            "unavailable_replicas": unavailable,
            "conditions": conditions,
        }

        if not _deployment_status(deployment):
            unhealthy_deployments.append(deployment)

    return {
        "healthy": len(unhealthy_deployments) == 0,
        "total_deployments": len(items),
        "unhealthy_deployments": unhealthy_deployments,
    }
