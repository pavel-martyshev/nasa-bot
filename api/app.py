import asyncio
from typing import cast

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response

from api.origin_filter_middleware import ALLOWED_ORIGINS, OriginFilterMiddleware
from config import app_settings
from database.postgres.core import init_db
from database.postgres.core.CRUD.apod import APODCRUD
from database.postgres.core.protocols import APODProtocol

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(OriginFilterMiddleware)

crud = APODCRUD()


@app.get("/apodExplanation")
async def apod_explanation(apod_id: int, language_code: str) -> Response:
    apod = cast(APODProtocol | None, await crud.get(id=apod_id))

    if not apod:
        return JSONResponse(status_code=404, content={"detail": "APOD not found"})

    title = apod.title_ru if language_code == "ru" else apod.title
    explanation = apod.explanation_ru if language_code == "ru" else apod.explanation

    return JSONResponse({"title": title, "explanation": explanation})


if __name__ == '__main__':
    asyncio.run(init_db())
    uvicorn.run(app, host=app_settings.api.bot_api_host, port=app_settings.api.bot_api_port)
