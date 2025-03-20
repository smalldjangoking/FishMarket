from aiogram import Bot, Dispatcher, types
from django.conf import settings
from typing import Callable, Dict, Any, Awaitable

from telegram.handlers import router

API = settings.T_API

bot = Bot(token=API)
dp = Dispatcher()

# Список разрешённых пользователей
ALLOWED_USERS = {1750975759, }  # Можно заполнить из настроек или БД

async def auth_middleware(
    handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
    event: types.TelegramObject,
    data: Dict[str, Any]
) -> Any:
    if isinstance(event, types.Message):
        if event.from_user.id not in ALLOWED_USERS:
            await event.reply("⛔ У вас нет доступа к этому боту ⛔")
            return None
    return await handler(event, data)


dp.include_router(router)

dp.message.middleware(auth_middleware)
dp.callback_query.middleware(auth_middleware)