from fastapi import APIRouter
from src.json_handler import load_array_scenarios


router = APIRouter()


@router.get('/')
async def stop():
    table = list(load_array_scenarios())
    return {"scenarios": table, 'subject': 'scenarios', 'status': 'array'}
