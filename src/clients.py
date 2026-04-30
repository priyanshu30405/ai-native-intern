import json
import os
from typing import Any, Dict

import requests


class OpenRouterClient:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY", "")
        self.model = model or os.getenv(
            "OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct"
        )
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    @property
    def enabled(self) -> bool:
        return bool(self.api_key.strip())

    def complete_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        if not self.enabled:
            raise RuntimeError("OPENROUTER_API_KEY is missing.")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
        }
        response = requests.post(self.base_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        text = data["choices"][0]["message"]["content"]
        return json.loads(text)
