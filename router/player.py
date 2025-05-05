from fastapi import APIRouter
from player import Player
from src.json_handler import load_scenarios


router = APIRouter()


@router.get('/{scenario_name}/start')
async def start(scenario_name: str):
    player = Player()

    logs = load_scenarios(f'scenarios/{scenario_name}.json')
    player.start(logs, 0.3)
    return {"scenario_name": scenario_name, 'subject': 'player', 'status': 'start'}

@router.get('/{scenario_name}/stop')
async def stop(scenario_name: str):
    player = Player()

    player.stop()
    return {"scenario_name": scenario_name, 'subject': 'player', 'status': 'stop'}
