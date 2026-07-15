import shlex
import subprocess
from typing import Any

from loguru import logger

from core.config import settings


def build_kubectl_command(args: list[str], context: str | None = None) -> list[str]:
    command = ["kubectl"]
    if settings.kubeconfig_path:
        command += ["--kubeconfig", settings.kubeconfig_path]
    if context:
        command += ["--context", context]
    command += args
    return command


def run_kubectl(args: list[str], timeout: int = 30, context: str | None = None) -> dict[str, Any]:
    command = build_kubectl_command(args, context)
    logger.info("Running kubectl command: {}", " ".join(shlex.quote(item) for item in command))

    try:
        result = subprocess.run(
            command,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except FileNotFoundError:
        error_message = "kubectl executable not found. Install kubectl and ensure it is on PATH."
        logger.error("{}", error_message)
        return {
            "success": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": error_message,
            "command": command,
        }
    except subprocess.TimeoutExpired as exc:
        error_message = f"kubectl command timed out after {timeout} seconds."
        logger.error("{}", error_message)
        return {
            "success": False,
            "exit_code": -1,
            "stdout": exc.stdout or "",
            "stderr": error_message,
            "command": command,
        }
    except Exception as exc:
        error_message = f"Unexpected kubectl error: {exc}"
        logger.error("{}", error_message)
        return {
            "success": False,
            "exit_code": -1,
            "stdout": "",
            "stderr": error_message,
            "command": command,
        }

    stdout = result.stdout.strip() if result.stdout else ""
    stderr = result.stderr.strip() if result.stderr else ""
    success = result.returncode == 0

    if not success:
        logger.warning("kubectl command failed: {}", stderr or stdout)

    return {
        "success": success,
        "exit_code": result.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "command": command,
    }
