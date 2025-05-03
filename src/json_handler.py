import json
from typing import Any
from datetime import datetime

def load_json(filepath: str) -> dict[str, Any]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath: str, data: dict[str, Any]) -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_scenarios(filepath: str):
    content = load_json(filepath)
    return content.get("scenario", [])

def save_scenarios(logs: list):
    created_at = datetime.now().strftime("%Y%m%d%H%M%S")
    save_json(f'scenarios/recorded_{created_at}.json', {"scenario": logs})
