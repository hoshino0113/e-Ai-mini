import json
import requests
from app.prompts import SYSTEM_PROMPT


def extract_json(text: str) -> dict:
    text = text.strip()

    if text.startswith("```json"):
        text = text.removeprefix("```json").removesuffix("```").strip()
    elif text.startswith("```"):
        text = text.removeprefix("```").removesuffix("```").strip()

    return json.loads(text)


class OllamaClient:
    def __init__(self, model: str = "deepseek-r1:14b"):
        self.model = model
        self.url = "http://localhost:11434/api/chat"

    def decide_tool(self, question: str) -> dict:
        payload = {
            "model": self.model,
            "stream": False,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
            "options": {
                "temperature": 0
            }
        }

        response = requests.post(self.url, json=payload, timeout=120)
        response.raise_for_status()

        content = response.json()["message"]["content"]

        try:
            return extract_json(content)
        except json.JSONDecodeError:
            return {
                "tool": "none",
                "reason": "Model did not return valid JSON.",
                "input": question,
                "raw_response": content
            }