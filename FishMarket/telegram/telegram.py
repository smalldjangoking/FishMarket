import asyncio

from aiogram import Bot, Dispatcher
from django.conf import settings

from telegram.handlers import router

API = settings.T_API

bot = Bot(token=API)
dp = Dispatcher()
dp.include_router(router)