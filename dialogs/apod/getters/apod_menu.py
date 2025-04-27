from datetime import datetime

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import User
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from icecream import ic
from mistralai import Mistral
import yt_dlp

from config import config
from http_client.aiohttp_client import HttpClient


async def handle_explanation(explanation: str, command: str):
    api_key = config.mistral_api_key
    model = "mistral-small-latest"

    client = Mistral(api_key=api_key)

    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                "role": "user",
                "content": command + " No additional offers.",
            },
            {
                "role": "user",
                "content": explanation,
            },
        ]
    )

    return chat_response.choices[0].message.content


async def getter(event_from_user: User, dialog_manager: DialogManager, bot: Bot, **_):
    url: str = config.nasa_api_base_url + f"/planetary/apod?api_key={config.nasa_api_key}"

    if dialog_manager.dialog_data.get("apod_date"):
        url += f"&date={dialog_manager.dialog_data.pop('apod_date')}"
    elif dialog_manager.dialog_data.pop("random_apod", False):
        url += f"&count=1"

    apod_data = await HttpClient.get_apod(url=url)

    if isinstance(apod_data, list):
        apod_data = apod_data[0]

    if apod_data["media_type"] == "image":
        url_key = "url" if apod_data["url"].endswith(".png") else "hdurl"
        media = MediaAttachment(ContentType.PHOTO, apod_data[url_key])
    else:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(apod_data["url"], download=False)
            media = MediaAttachment(ContentType.VIDEO, info.get("url", None))

    if event_from_user.language_code == "ru":
        date_format = "%d.%m.%Y"
        command = f"Translate to Russian next message. But send only the translation. No additional offers."
        explanation = await handle_explanation(apod_data["explanation"], command)
    else:
        date_format = "%d/%m/%Y"
        explanation = apod_data["explanation"]

    date = datetime.strftime(datetime.strptime(apod_data["date"], "%Y-%m-%d"), date_format)

    if len(explanation) > 1024:
        command = ("Shorten the text so that it retains the meaning, but is no more than 1024 characters long. "
                   "But send only the shortened message.")
        explanation = await handle_explanation(explanation, command)

    return {"date": date, "explanation": explanation, "media": media}
