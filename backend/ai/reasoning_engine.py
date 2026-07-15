import json
from typing import Any

from loguru import logger

from .llm_client import call_openrouter
from .prompt_builder import build_investigation_prompt, build_system_prompt


async def analyze_investigation(investigation_data: dict[str, Any]) -> dict[str, Any]:
    """Analyze investigation data using LLM to find root cause."""
    system_prompt = build_system_prompt()
    user_prompt = build_investigation_prompt(investigation_data)

    logger.info("Starting root cause analysis with LLM")
    result = await call_openrouter(system_prompt, user_prompt)

    if not result["success"]:
        logger.error("LLM call failed: {}", result["error"])
        return {
            "success": False,
            "error": result["error"],
            "root_cause": None,
            "explanation": None,
            "fix": None,
            "kubectl_command": None,
            "prevention": None,
            "confidence": 0,
        }

    try:
        response_text = result["response"]
        json_start = response_text.find("{")
        json_end = response_text.rfind("}") + 1

        if json_start >= 0 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            parsed = json.loads(json_str)
        else:
            logger.warning("Could not extract JSON from LLM response")
            parsed = {
                "root_cause": "Unable to determine root cause",
                "explanation": response_text,
                "suggested_fix": "Please review logs manually",
                "kubectl_command": "kubectl describe deployment <name>",
                "prevention": "Enable monitoring and alerting",
                "confidence": 0,
            }

        return {
            "success": True,
            "error": None,
            "root_cause": parsed.get("root_cause", "Unknown"),
            "explanation": parsed.get("explanation", ""),
            "fix": parsed.get("suggested_fix", ""),
            "kubectl_command": parsed.get("kubectl_command", ""),
            "prevention": parsed.get("prevention", ""),
            "confidence": parsed.get("confidence", 0),
        }

    except json.JSONDecodeError as exc:
        logger.error("Failed to parse LLM JSON response: {}", exc)
        return {
            "success": False,
            "error": "Failed to parse LLM response",
            "root_cause": None,
            "explanation": None,
            "fix": None,
            "kubectl_command": None,
            "prevention": None,
            "confidence": 0,
        }
    except Exception as exc:
        logger.error("Unexpected error analyzing investigation: {}", exc)
        return {
            "success": False,
            "error": f"Unexpected error: {exc}",
            "root_cause": None,
            "explanation": None,
            "fix": None,
            "kubectl_command": None,
            "prevention": None,
            "confidence": 0,
        }
