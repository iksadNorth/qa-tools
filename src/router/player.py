from fastapi import APIRouter
from src.js_bridge.player import Player
from src.json_handler import load_scenarios

import time
from uuid import uuid4


router = APIRouter()


@router.get('/{scenario_name}/start')
async def start(scenario_name: str, cursor: str = None):
    player = Player()
    player_id = uuid4()

    logs = load_scenarios(scenario_name)
    
    # cursor 파라미터 적용
    for idx, log in enumerate(logs):
        if not cursor: break
        if log.get('step_id') == cursor: break
    logs = logs[idx:]
    
    for log in player.start(logs, scenario_name, player_id):
        time.sleep(0.2)
    
    return {"scenario_name": scenario_name, 'subject': 'player', 'status': 'start'}

def load_step(scenario_name: str, cursor: str = None):
    logs = load_scenarios(scenario_name)
    
    # cursor 파라미터 적용
    log, next_cursor = None, None
    for idx, log in enumerate(logs):
        if not cursor: break
        if log.get('step_id') == cursor: break
    if len(logs)-1 >= idx+1:
        next_cursor = logs[idx+1].get('step_id')
    
    return log, next_cursor

@router.get('/{scenario_name}/step')
async def step(scenario_name: str, cursor: str = None):
    player = Player()
    log, next_cursor = load_step(scenario_name, cursor)
    player.start_unit(log)
    
    result = {"scenario_name": scenario_name, 'subject': 'player', 'status': 'step'}
    if next_cursor:
        result['cursor'] = next_cursor
    
    return result

@router.get('/{scenario_name}/stop')
async def stop(scenario_name: str):
    player = Player()

    player.stop()
    return {"scenario_name": scenario_name, 'subject': 'player', 'status': 'stop'}
