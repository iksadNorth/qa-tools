from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import CONFIG

def add_cors_middleware(app: FastAPI):
    origins: list = CONFIG.get('APP.CORS.ORIGINS')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
