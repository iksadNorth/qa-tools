from fastapi import FastAPI
from router import player, recorder
from src.lifespan import lifespan


app = FastAPI(lifespan=lifespan)


# Router 정의
app.include_router(player.router, prefix="/player")
app.include_router(recorder.router, prefix="/recorder")
