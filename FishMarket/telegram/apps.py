import asyncio
import os
import sys
import threading
import logging
from django.apps import AppConfig


class TelegramConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram'
    bot_started = False

    def ready(self):
        if 'runserver' not in sys.argv:
            return

        if self.bot_started:
            return

        if os.environ.get('RUN_MAIN') != 'true':
            return

        from . import telegram

        async def start_bot():
            print('Starting bot...')
            await telegram.dp.start_polling(telegram.bot)

        def run_bot():
            logging.basicConfig(level=logging.INFO)
            try:
                asyncio.run(start_bot())
            except KeyboardInterrupt:
                print('Stopping bot...')


        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        self.bot_started = True
