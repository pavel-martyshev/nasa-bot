from typing import cast

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from multidict import MultiMapping

from database.postgres.core.CRUD.apod import ApodCrud
from database.postgres.core.protocols import ApodProtocol

crud = ApodCrud()


async def apod_explanation(request: Request) -> Response:
    """
    Retrieve APOD title and explanation in the specified language.

    Args:
        request (Request): Aiohttp request object containing query parameters:
            - apod_id (str): ID of the APOD entry to retrieve.
            - language_code (str): Language code for localization ("ru" for Russian, any other value defaults to
             English).

    Returns:
        Response: JSON with title and explanation, or 404 if not found.
    """
    query: MultiMapping[str] = request.query

    apod_id: str = query.get("apod_id", "")
    language_code: str = query.get("language_code", "")

    apod = cast(ApodProtocol | None, await crud.get(id=apod_id))

    if not apod:
        return web.json_response({"detail": "APOD not found"}, status=404)

    title = apod.title_ru if language_code == "ru" else apod.title
    explanation = apod.explanation_ru if language_code == "ru" else apod.explanation

    return web.json_response({"title": title, "explanation": explanation}, status=200)
