import json
from typing import Any

import httpx
from loguru import logger

from core.config import settings


async def call_openrouter(system_prompt: str, user_prompt: str) -> dict[str, Any]:
    """Call OpenRouter API for LLM reasoning."""
    if not settings.openrouter_api_key:
        logger.error("OPENROUTER_API_KEY not configured")
        return {
            "success": False,
            "error": "OpenRouter API key not configured",
            "response": None,
        }

    if not settings.openrouter_model:
        logger.error("OPENROUTER_MODEL not configured")
        return {
            "success": False,
            "error": "OpenRouter model not configured",
            "response": None,
        }

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.openrouter_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.3,
        "max_tokens": 2000,
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()

            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0].get("message", {}).get("content", "")
                logger.info("OpenRouter API call succeeded")
                return {
                    "success": True,
                    "error": None,
                    "response": content,
                }
            else:
                logger.warning("Unexpected OpenRouter response structure")
                return {
                    "success": False,
                    "error": "Invalid response structure from OpenRouter",
                    "response": None,
                }

    except httpx.HTTPStatusError as exc:
        logger.error("OpenRouter API HTTP error: {}", exc.response.status_code)
        return {
            "success": False,
            "error": f"OpenRouter API error: {exc.response.status_code}",
            "response": None,
        }
    except httpx.TimeoutException:
        logger.error("OpenRouter API timeout")
        return {
            "success": False,
            "error": "OpenRouter API timeout",
            "response": None,
        }
    except Exception as exc:
        logger.error("Unexpected OpenRouter error: {}", exc)
        return {
            "success": False,
            "error": f"Unexpected error: {exc}",
            "response": None,
        }
