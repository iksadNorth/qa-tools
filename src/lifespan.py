from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from src.driver_factory import SeleniumDriverFactory
from src.js_bridge.recorder import Recorder
from src.js_bridge.player import Player
from src.config import CONFIG


@asynccontextmanager
async def lifespan(app: FastAPI):
    driver = SeleniumDriverFactory().get_driver()
    driver.get(CONFIG.get('APP.SELENIUM.INIT_URL'))
    recorder = Recorder(driver=driver)
    player = Player(driver=driver)

    print("JS 코드 주입")
    task_recorder = asyncio.create_task(recorder.launch(1))
    task_player = asyncio.create_task(player.launch(1))
    print("JS 코드 주입 완료")

    try:
        yield # FastAPI 프로세스 가동
    except Exception:
        print('Terminate Gracefully!')

    print("앱 종료 중...")
    task_recorder.cancel()
    task_player.cancel()
    await asyncio.gather(
        task_recorder, 
        task_player, 
        return_exceptions=True
    )
    driver.quit()

    print("WebDriver 종료")
