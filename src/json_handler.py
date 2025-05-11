import json
from typing import Any
from datetime import datetime
import os
import platform
from pathlib import Path
from src.config import CONFIG


SCENARIO_DIR = CONFIG.get('APP.SCENARIO.ROOTDIR')

def load_json(filepath: str) -> dict[str, Any]:
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath: str, data: dict[str, Any]) -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def ensure_dir_exists(path: str):
    """디렉터리가 없으면 생성"""
    os.makedirs(path, exist_ok=True)
    
    system = platform.system()
    if system in {"Linux", "Darwin"}:
        try:
            uid = os.getuid()
            gid = os.getgid()
            os.chown(path, uid, gid)
        except PermissionError:
            print(f"⚠️ {path} 권한을 변경하려면 루트 권한이 필요합니다.")

def get_scenario_path(scenario_name: str = None) -> str:
    """시나리오 저장 경로 생성"""
    ensure_dir_exists(SCENARIO_DIR)
    if scenario_name:
        return os.path.join(SCENARIO_DIR, f"{scenario_name}.json")
    else:
        created_at = datetime.now().strftime("%Y%m%d%H%M%S")
        return os.path.join(SCENARIO_DIR, f"recorded_{created_at}.json")

def load_scenarios(scenario_name: str):
    filepath = get_scenario_path(scenario_name)
    content = load_json(filepath)
    return content.get("scenario", [])

def save_scenarios(logs: list, scenario_name: str = None):
    filepath = get_scenario_path(scenario_name)
    save_json(filepath, {"scenario": logs})

def load_array_scenarios():
    """존재는 시나리오 목록 출력
    """
    ensure_dir_exists(SCENARIO_DIR)
    
    def get_name(items: str):
        items = str(items)
        _, _, name = items.partition('/')
        name, _, _ = name.partition('.')
        return name
    yield from map(get_name, Path(SCENARIO_DIR).rglob('*.json'))
