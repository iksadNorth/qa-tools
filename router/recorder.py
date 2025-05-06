from fastapi import APIRouter
from js_bridge.recorder import Recorder
from src.json_handler import save_scenarios


router = APIRouter()


@router.get('/{scenario_name}/start')
async def start(scenario_name: str, url: str = None):
    recorder = Recorder()
    recorder.start()
    if url: recorder.driver.get(url)
    return {"scenario_name": scenario_name, 'subject': 'recorder', 'status': 'start'}

@router.get('/{scenario_name}/stop')
async def stop(scenario_name: str):
    recorder = Recorder()

    logs = recorder.getLog()
    save_scenarios(logs, scenario_name)

    recorder.stop()
    return {"scenario_name": scenario_name, 'subject': 'recorder', 'status': 'stop'}
