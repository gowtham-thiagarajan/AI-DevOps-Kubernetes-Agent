from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
import json
import asyncio

from ai.reasoning_engine import analyze_investigation
from models.schemas import DiagnosisPayload
from models.schemas import InvestigationResponse
from services.investigation import run_investigation, run_investigation_stream
from services.history import save_investigation, get_investigations

router = APIRouter()


@router.post("/investigate", response_model=InvestigationResponse)
async def investigate(context: str | None = Query(None)) -> InvestigationResponse:
    try:
        investigation = run_investigation(context=context)

        # Check for kubectl / cluster errors in investigation evidence
        error_messages = []
        pods_err = investigation.get("pods", {}).get("error")
        if pods_err:
            error_messages.append(f"Pods: {pods_err}")
        # logs may include errors
        logs_err = investigation.get("logs", {}).get("error") if isinstance(investigation.get("logs"), dict) else None
        if logs_err:
            error_messages.append(f"Logs: {logs_err}")

        if error_messages:
            # Return friendly diagnosis for connectivity / kube issues
            friendly = "Unable to connect to Kubernetes cluster or run kubectl commands.\n\nPlease verify:\n- kubeconfig path is correct\n- kubectl is installed and on PATH\n- current user has cluster access (kubectl get pods)"
            diagnosis = DiagnosisPayload(
                root_cause="Unable to connect to Kubernetes cluster",
                explanation="\n".join(error_messages),
                fix=friendly,
                kubectl_command="kubectl config view --minify; kubectl get pods -A",
                prevention="Ensure kubeconfig and permissions are configured for this user.",
                confidence=0,
            )
            return InvestigationResponse(status="error", investigation=investigation, diagnosis=diagnosis)

        diagnosis_data = await analyze_investigation(investigation)

        diagnosis = None
        if diagnosis_data.get("success"):
            diagnosis = DiagnosisPayload(
                root_cause=diagnosis_data.get("root_cause", "Unknown"),
                explanation=diagnosis_data.get("explanation", ""),
                fix=diagnosis_data.get("fix", ""),
                kubectl_command=diagnosis_data.get("kubectl_command", ""),
                prevention=diagnosis_data.get("prevention", ""),
                confidence=diagnosis_data.get("confidence", 0),
            )
            # Save to history
            save_investigation(
                root_cause=diagnosis.root_cause,
                explanation=diagnosis.explanation,
                confidence=diagnosis.confidence,
            )

        return InvestigationResponse(
            status="success",
            investigation=investigation,
            diagnosis=diagnosis,
        )
    except Exception as exc:
        return InvestigationResponse(
            status="error",
            investigation={},
            diagnosis=None,
        )


@router.get("/investigate/stream")
async def investigate_stream(context: str | None = Query(None)):
    """Server-Sent Events stream for realtime investigation progress.

    Streams progress events and posts a final `diagnosis` event when AI analysis completes.
    """

    async def event_generator():
        # run_investigation_stream yields SSE-ready `data: ...\n\n` strings
        for chunk in run_investigation_stream(context=context):
            # forward step/result chunks
            yield chunk
            await asyncio.sleep(0)

            # try to parse, if this is the final result then run AI analysis
            try:
                text = chunk.strip()
                if text.startswith("data:"):
                    payload = json.loads(text[len("data:"):].strip())
                    if payload.get("type") == "result":
                        investigation = payload.get("payload")
                        diagnosis_data = await analyze_investigation(investigation)
                        # save history if diagnosis succeeded
                        if diagnosis_data.get("success"):
                            save_investigation(
                                root_cause=diagnosis_data.get("root_cause", "Unknown"),
                                explanation=diagnosis_data.get("explanation", ""),
                                confidence=diagnosis_data.get("confidence", 0),
                            )

                        yield f"data: {json.dumps({'type': 'diagnosis', 'payload': diagnosis_data})}\n\n"
            except Exception:
                # ignore parsing errors and continue streaming
                continue

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/history")
async def get_history(limit: int = 10):
    """Get recent investigations from history."""
    investigations = get_investigations(limit=limit)
    return {
        "status": "success",
        "investigations": investigations,
        "total": len(investigations),
    }


