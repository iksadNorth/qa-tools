from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader
from src.config import CONFIG


router = APIRouter()


@router.get('/', response_class=HTMLResponse)
async def form():
    env = Environment(loader=FileSystemLoader(CONFIG.get('APP.JS.ROOTDIR')))
    template = env.get_template('controller.html')
    rendered_script = template.render()
    return rendered_script
