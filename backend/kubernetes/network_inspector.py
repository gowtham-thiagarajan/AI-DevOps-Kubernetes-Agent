import json
from typing import Any

from loguru import logger

from .kubectl_executor import run_kubectl


def _index_endpoints(payload: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    result: dict[tuple[str, str], dict[str, Any]] = {}
    for item in payload.get("items", []) or []:
        metadata = item.get("metadata", {})
        namespace = metadata.get("namespace", "default")
        name = metadata.get("name", "unknown")
        result[(namespace, name)] = item
    return result


def inspect_network() -> dict[str, Any]:
    svc_result = run_kubectl(["get", "svc", "-A", "-o", "json"])
    ep_result = run_kubectl(["get", "endpoints", "-A", "-o", "json"])

    if not svc_result["success"]:
        return {
            "healthy": False,
            "service_issues": [],
            "error": svc_result["stderr"] or svc_result["stdout"],
        }

    if not ep_result["success"]:
        return {
            "healthy": False,
            "service_issues": [],
            "error": ep_result["stderr"] or ep_result["stdout"],
        }

    try:
        svc_payload = json.loads(svc_result["stdout"])
        ep_payload = json.loads(ep_result["stdout"])
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse service or endpoint JSON: {}", exc)
        return {
            "healthy": False,
            "service_issues": [],
            "error": "Failed to parse kubectl service or endpoint output.",
        }

    endpoints_by_name = _index_endpoints(ep_payload)
    service_issues: list[dict[str, Any]] = []
    items = svc_payload.get("items", []) or []

    for item in items:
        metadata = item.get("metadata", {})
        spec = item.get("spec", {})
        namespace = metadata.get("namespace", "default")
        name = metadata.get("name", "unknown")
        selector = spec.get("selector") or {}
        service_type = spec.get("type", "ClusterIP")

        if not selector:
            continue

        endpoint = endpoints_by_name.get((namespace, name))
        subsets = endpoint.get("subsets") if endpoint else None
        if not endpoint or not subsets:
            service_issues.append(
                {
                    "name": name,
                    "namespace": namespace,
                    "service_type": service_type,
                    "selector": selector,
                    "issue": "Missing endpoints or selector does not match any pods",
                }
            )

    return {
        "healthy": len(service_issues) == 0,
        "total_services": len(items),
        "service_issues": service_issues,
    }
