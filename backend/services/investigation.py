from kubernetes.pod_inspector import inspect_pods
from kubernetes.logs_collector import collect_logs
from kubernetes.events_analyzer import analyze_events
from kubernetes.deployment_inspector import inspect_deployments
from kubernetes.network_inspector import inspect_network
import json
from typing import Generator


def run_investigation(context: str | None = None) -> dict[str, object]:
    """Run a full investigation and return collected evidence."""
    pods = inspect_pods()
    logs = collect_logs(pods.get("problematic_pods", []))
    events = analyze_events()
    deployments = inspect_deployments()
    network = inspect_network()

    return {
        "pods": pods,
        "logs": logs,
        "events": events,
        "deployments": deployments,
        "network": network,
    }


def run_investigation_stream(context: str | None = None) -> Generator[str, None, None]:
    """Generator that yields Server-Sent Events (SSE) style text chunks.

    Yields progress events as JSON strings prefixed for SSE consumption.
    Final event is of type `result` containing the full investigation payload.
    """
    def sse_event(event_type: str, payload: dict) -> str:
        return f"data: {json.dumps({'type': event_type, 'payload': payload})}\n\n"

    # Step 1: pods
    yield sse_event("step", {"step": "Checking Pods"})
    pods = inspect_pods()
    yield sse_event("step_result", {"step": "Checking Pods", "result": pods})

    # Step 2: logs
    yield sse_event("step", {"step": "Reading Logs"})
    logs = collect_logs(pods.get("problematic_pods", []))
    yield sse_event("step_result", {"step": "Reading Logs", "result": {"count": len(logs)}})

    # Step 3: events
    yield sse_event("step", {"step": "Analyzing Events"})
    events = analyze_events()
    yield sse_event("step_result", {"step": "Analyzing Events", "result": events})

    # Step 4: deployments
    yield sse_event("step", {"step": "Inspecting Deployments"})
    deployments = inspect_deployments()
    yield sse_event("step_result", {"step": "Inspecting Deployments", "result": deployments})

    # Step 5: networking
    yield sse_event("step", {"step": "Checking Networking"})
    network = inspect_network()
    yield sse_event("step_result", {"step": "Checking Networking", "result": network})

    # Final combined payload
    investigation = {
        "pods": pods,
        "logs": logs,
        "events": events,
        "deployments": deployments,
        "network": network,
    }

    yield sse_event("result", investigation)
