import json
from typing import Any

from loguru import logger

from .kubectl_executor import run_kubectl

EVENT_FILTER_TERMS = [
    "FailedScheduling",
    "BackOff",
    "FailedMount",
    "FailedPull",
    "ErrImagePull",
    "Unhealthy",
]


def _matches_event_reason(reason: str) -> bool:
    normalized = reason or ""
    for term in EVENT_FILTER_TERMS:
        if term.lower() in normalized.lower():
            return True
    return False


def analyze_events() -> dict[str, Any]:
    result = run_kubectl(["get", "events", "-A", "-o", "json"])
    if not result["success"]:
        return {
            "summary": [],
            "total_events": 0,
            "error": result["stderr"] or result["stdout"],
        }

    try:
        payload = json.loads(result["stdout"])
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse events JSON: {}", exc)
        return {
            "summary": [],
            "total_events": 0,
            "error": "Failed to parse kubectl events output.",
        }

    items = payload.get("items", [])
    grouped: dict[tuple[str, str], dict[str, Any]] = {}
    total_events = len(items)

    for item in items:
        metadata = item.get("metadata", {})
        reason = item.get("reason") or "Unknown"
        namespace = metadata.get("namespace", "default")
        message = item.get("message", "")

        if not _matches_event_reason(reason):
            continue

        key = (namespace, reason)
        if key not in grouped:
            grouped[key] = {
                "namespace": namespace,
                "reason": reason,
                "count": 0,
                "messages": [],
            }

        grouped[key]["count"] += 1
        if message and len(grouped[key]["messages"]) < 5:
            grouped[key]["messages"].append(message)

    summary = sorted(grouped.values(), key=lambda item: (-item["count"], item["reason"]))

    return {
        "summary": summary,
        "total_events": total_events,
        "matched_events": sum(item["count"] for item in summary),
    }
