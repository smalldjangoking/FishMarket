import asyncio

from asgiref.sync import async_to_sync
from celery import shared_task
from django.conf import settings
import logging

from telegram import telegram
from telegram.helpers import get_order_by_id, prepare_order_message_and_keyboard


@shared_task
def send_telegram_notification(order_id):
    try:
        get_order = async_to_sync(get_order_by_id)(order_id)
        text, kb = prepare_order_message_and_keyboard(get_order)
        bot = telegram.Bot(token=settings.TELEGRAM_API)
        async_to_sync(bot.send_message)(
            chat_id=settings.TELEGRAM_ID,
            text=text,
            reply_markup=kb.as_markup(),
            parse_mode="HTML"
        )
        return f"Message sent to Telegram for order {order_id}"

    except Exception as e:
        logging.error(f"Error sending Telegram notification for order {order_id}: {e}")