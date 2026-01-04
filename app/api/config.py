from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware

from app.database.config import URL_DB

class InicializeApi:
    def __init__(self, app):
        self.app = app
        self.execute_routers_api()

    def execute_routers_api(self):
        from app.api.routers import router as api_router

        self.app.include_router(api_router, prefix="/api")

        self.app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:8044",
            "http://192.168.3.28:8044",
            "http://127.0.0.1:8044",
            "http://192.168.3.28",
            "http://192.168.2.46",
        ],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        )

        register_tortoise(
        self.app,
        db_url= URL_DB,
        modules={"models": ["app.database.models"]},
        add_exception_handlers=True,
        )
