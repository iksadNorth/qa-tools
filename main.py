from fastapi import FastAPI
from router import player, recorder
from src.lifespan import lifespan
from middlewares.cors import add_cors_middleware


app = FastAPI(lifespan=lifespan)


# Middleware 정의
add_cors_middleware(app)

# Router 정의
app.include_router(player.router, prefix="/api/v1/player")
app.include_router(recorder.router, prefix="/api/v1/recorder")
