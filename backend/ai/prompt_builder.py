from typing import Any


def build_system_prompt() -> str:
    """Build the system prompt for the AI Kubernetes troubleshooter."""
    return """You are a Senior Kubernetes Site Reliability Engineer (SRE) with 10+ years of experience troubleshooting Kubernetes clusters.

Your role is to analyze Kubernetes investigation data and provide:
1. Root Cause - the underlying issue
2. Explanation - why this happened
3. Suggested Fix - actionable steps to resolve
4. Kubectl Commands - exact commands to run
5. Prevention - how to prevent this in future
6. Confidence Score - how confident you are (0-100)

When analyzing evidence:
- Correlate multiple signals (pod status, logs, events, deployments)
- Look for patterns and root causes, not just symptoms
- Provide practical, beginner-friendly recommendations
- Include exact kubectl commands when possible
- Be specific, not generic

Format your response as JSON with this structure:
{
    "root_cause": "string - the underlying issue",
    "explanation": "string - why this happened",
    "suggested_fix": "string - how to fix it",
    "kubectl_command": "string - exact kubectl command or series of commands",
    "prevention": "string - how to prevent this in future",
    "confidence": integer between 0 and 100
}
"""


def build_investigation_prompt(investigation_data: dict[str, Any]) -> str:
    """Build a prompt from investigation data."""
    pod_info = investigation_data.get("pods", {})
    log_info = investigation_data.get("logs", {})
    event_info = investigation_data.get("events", {})
    deployment_info = investigation_data.get("deployments", {})
    network_info = investigation_data.get("network", {})

    prompt = "Please analyze the following Kubernetes cluster investigation data and find the root cause:\n\n"

    prompt += "## Pod Status\n"
    if pod_info.get("problematic_pods"):
        for pod in pod_info["problematic_pods"]:
            prompt += f"- Pod: {pod.get('name')} in namespace {pod.get('namespace')}\n"
            prompt += f"  Status: {pod.get('status')}\n"
    else:
        prompt += "- All pods healthy\n"
    prompt += f"Total pods: {pod_info.get('total_pods', 0)}\n"
    prompt += f"Healthy: {pod_info.get('healthy', True)}\n\n"

    prompt += "## Logs\n"
    if log_info.get("pod_logs"):
        for log in log_info["pod_logs"]:
            prompt += f"- Pod: {log.get('name')} ({log.get('status')})\n"
            prompt += f"  Log excerpt:\n{log.get('log_excerpt', 'No logs')}\n"
    else:
        prompt += "- No problematic pod logs\n"
    prompt += "\n"

    prompt += "## Events\n"
    if event_info.get("summary"):
        for event in event_info["summary"]:
            prompt += f"- {event.get('reason')} in {event.get('namespace')}\n"
            prompt += f"  Count: {event.get('count')}\n"
            if event.get("messages"):
                prompt += f"  Messages: {event['messages'][0]}\n"
    else:
        prompt += "- No significant events\n"
    prompt += f"Total events: {event_info.get('total_events', 0)}\n\n"

    prompt += "## Deployments\n"
    if deployment_info.get("unhealthy_deployments"):
        for deployment in deployment_info["unhealthy_deployments"]:
            prompt += f"- {deployment.get('name')} in {deployment.get('namespace')}\n"
            prompt += f"  Desired: {deployment.get('desired_replicas')}, Available: {deployment.get('available_replicas')}\n"
    else:
        prompt += "- All deployments healthy\n"
    prompt += f"Total deployments: {deployment_info.get('total_deployments', 0)}\n\n"

    prompt += "## Networking\n"
    if network_info.get("service_issues"):
        for issue in network_info["service_issues"]:
            prompt += f"- Service: {issue.get('name')} in {issue.get('namespace')}\n"
            prompt += f"  Issue: {issue.get('issue')}\n"
    else:
        prompt += "- All services and networking healthy\n"
    prompt += f"Total services: {network_info.get('total_services', 0)}\n\n"

    prompt += "Based on this evidence, what is the root cause of any issues?"

    return prompt
