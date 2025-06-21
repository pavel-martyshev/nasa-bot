from aiogram import Bot
from aiogram.enums import ChatAction


class ChatActionSender:
    """
    Sends appropriate 'chat action' (e.g. 'uploading photo') to indicate that the bot is processing media.
    """

    def __init__(self, chat_id: int, bot: Bot) -> None:
        self._chat_id = chat_id
        self._bot = bot

    async def send_chat_action(self, media_type: str) -> None:
        """
        Send an appropriate chat action based on media type.

        Args:
            media_type (str): Type of media being sent ("image" or "video").
        """

        if media_type == "image":
            chat_action = ChatAction.UPLOAD_PHOTO
        elif media_type == "video":
            chat_action = ChatAction.UPLOAD_VIDEO
        else:
            chat_action = None

        if chat_action:
            await self._bot.send_chat_action(self._chat_id, chat_action)
