import asyncio
from typing import cast

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, Response

from api.origin_filter_middleware import AllowedOriginsMiddleware
from config import app_settings
from database.postgres.core import init_db
from database.postgres.core.CRUD.apod import ApodCrud
from database.postgres.core.protocols import ApodProtocol

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AllowedOriginsMiddleware)

crud = ApodCrud()


@app.get("/apodExplanation")
async def apod_explanation(apod_id: int, language_code: str) -> Response:
    """
    Retrieve APOD title and explanation in the specified language.

    Args:
        apod_id (int): ID of the APOD entry to fetch.
        language_code (str): Language code ("ru" for Russian, anything else for English).

    Returns:
        Response: JSON with title and explanation, or 404 if not found.
    """
    apod = cast(ApodProtocol | None, await crud.get(id=apod_id))

    if not apod:
        return JSONResponse(status_code=404, content={"detail": "APOD not found"})

    title = apod.title_ru if language_code == "ru" else apod.title
    explanation = apod.explanation_ru if language_code == "ru" else apod.explanation

    return JSONResponse({"title": title, "explanation": explanation})


if __name__ == '__main__':
    asyncio.run(init_db())
    uvicorn.run(app, host=app_settings.api.bot_api_host, port=app_settings.api.bot_api_port)
