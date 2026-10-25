"""
Sloth Digest — Localhost Ollama LLM Client
Interacts strictly with local Ollama on localhost:11434.
No external network access allowed.
"""

import json
import re
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from backend.config import OLLAMA_HOST, DEFAULT_MODEL, REQUEST_TIMEOUT_SECONDS
from backend.models import SystemHealth


def check_ollama(model_name: Optional[str] = None) -> SystemHealth:
    """
    Pings local Ollama server, lists available models, and checks if target model is ready.
    """
    target_model = model_name or DEFAULT_MODEL
    url = f"{OLLAMA_HOST}/api/tags"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "SlothDigest/1.0"})
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = [m.get("name", "") for m in data.get("models", [])]
            # Match either exact name or base tag (e.g. qwen2.5:1.5b)
            model_present = any(
                target_model == m or target_model == m.split(":")[0] or m.startswith(target_model)
                for m in models
            )

            return SystemHealth(
                status="ready" if model_present else "model_missing",
                is_offline=True,
                ollama_connected=True,
                active_model=target_model,
                available_models=models,
                host=OLLAMA_HOST,
                error_message=None if model_present else f"Model '{target_model}' not found in Ollama. Run: ollama pull {target_model}"
            )
    except urllib.error.URLError as e:
        return SystemHealth(
            status="unreachable",
            is_offline=True,
            ollama_connected=False,
            active_model=target_model,
            available_models=[],
            host=OLLAMA_HOST,
            error_message="Cannot reach Ollama at localhost:11434. Ensure Ollama is installed and running."
        )
    except Exception as e:
        return SystemHealth(
            status="error",
            is_offline=True,
            ollama_connected=False,
            active_model=target_model,
            available_models=[],
            host=OLLAMA_HOST,
            error_message=str(e)
        )


def query_ollama_json(prompt: str, system_prompt: str, model_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Sends a prompt to local Ollama with JSON output formatting requested.
    Parses and returns the dictionary.
    """
    target_model = model_name or DEFAULT_MODEL
    url = f"{OLLAMA_HOST}/api/generate"

    payload = {
        "model": target_model,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.1,  # Low temperature for factual consistency
            "num_predict": 1024,
        }
    }

    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=req_data,
        headers={"Content-Type": "application/json", "User-Agent": "SlothDigest/1.0"}
    )

    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            raw_response = res_json.get("response", "{}")
            return extract_json_from_text(raw_response)
    except urllib.error.URLError as e:
        raise ConnectionError(f"Failed to communicate with local Ollama: {e}")
    except Exception as e:
        raise RuntimeError(f"Error querying local LLM: {e}")


def extract_json_from_text(text: str) -> Dict[str, Any]:
    """
    Safely extracts a JSON object from text, handling markdown fences and extraneous characters.
    """
    clean = text.strip()
    if clean.startswith("```"):
        clean = re.sub(r"^```(?:json)?\s*", "", clean)
        clean = re.sub(r"\s*```$", "", clean)

    # Find outermost curly braces
    start = clean.find("{")
    end = clean.rfind("}")
    if start != -1 and end != -1 and end > start:
        clean = clean[start : end + 1]

    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        # Fallback empty or partial recovery
        return {}
