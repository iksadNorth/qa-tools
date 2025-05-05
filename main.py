from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.driver_factory import SeleniumDriverFactory
import asyncio
from recorder import Recorder
from player import Player


@asynccontextmanager
async def lifespan(app: FastAPI):
    driver = SeleniumDriverFactory().get_driver()
    driver.get('https://www.naver.com/')
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

app = FastAPI(lifespan=lifespan)
