import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from icecream import ic
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from tortoise.contrib.pydantic import PydanticModel

from config import app_settings
from config.log_config import logger
from database.postgres.core import init_db
from database.postgres.core.CRUD.APOD import APODCRUD


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.warning("API started")

    yield

    logger.warning("API stopped")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nasa-bot-web-app.ru"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return JSONResponse({"status": "ok"})


@app.get("/apodExplanation")
async def apod_explanation(apod_id: int, language_code):
    apod: PydanticModel = await APODCRUD.get_apod(id=apod_id)

    title = apod.title_ru if language_code == "ru" else apod.title
    explanation = apod.explanation_ru if language_code == "ru" else apod.explanation

    return JSONResponse({"title": title, "explanation": explanation})


if __name__ == '__main__':
    asyncio.run(init_db())
    uvicorn.run(app, host=app_settings.api.bot_api_host, port=app_settings.api.bot_api_port)
