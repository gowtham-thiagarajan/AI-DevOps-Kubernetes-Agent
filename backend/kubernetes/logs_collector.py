from typing import Any

from .kubectl_executor import run_kubectl

LOG_KEYWORDS = [
    "exception",
    "traceback",
    "connection refused",
    "connection failed",
    "failed to connect",
    "env",
    "missing",
    "image pull",
    "imagepullbackoff",
    "imagepull",
    "startup",
    "error",
    "oomkilled",
]

MAX_LINES = 20
MAX_LENGTH = 3000


def _extract_relevant_lines(log_text: str) -> str:
    if not log_text:
        return ""

    lines = [line.strip() for line in log_text.splitlines() if line.strip()]
    matches = []
    for line in lines:
        lower = line.lower()
        if any(keyword in lower for keyword in LOG_KEYWORDS):
            matches.append(line)
            if len(matches) >= MAX_LINES:
                break

    if matches:
        return "\n".join(matches[:MAX_LINES])

    return "\n".join(lines[:MAX_LINES])


def _trim_log(log_text: str) -> str:
    if len(log_text) <= MAX_LENGTH:
        return log_text
    return log_text[:MAX_LENGTH].rstrip() + "\n...[truncated]"


def collect_logs(problematic_pods: list[dict[str, Any]]) -> dict[str, Any]:
    pod_logs: list[dict[str, Any]] = []

    for pod in problematic_pods:
        name = pod.get("name")
        namespace = pod.get("namespace")
        if not name or not namespace:
            continue

        result = run_kubectl(["logs", "-n", namespace, name, "--all-containers", "--tail", "200"])
        excerpt = ""
        source = "stdout"

        if result["success"] and result["stdout"]:
            excerpt = _extract_relevant_lines(result["stdout"])
        else:
            excerpt = result["stderr"] or result["stdout"] or "No logs available for this pod."
            source = "stderr"

        pod_logs.append(
            {
                "name": name,
                "namespace": namespace,
                "status": pod.get("status"),
                "log_excerpt": _trim_log(excerpt),
                "source": source,
            }
        )

    return {
        "pod_logs": pod_logs,
        "count": len(pod_logs),
    }
