import asyncio
import os
import sys
import multiprocessing
import logging

from django.apps import AppConfig


class TelegramConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram'
    bot_started = False

    def ready(self):
        import telegram.signals

        if 'runserver' not in sys.argv:
            return

        if self.bot_started:
            return

        if os.environ.get('RUN_MAIN') != 'true':
            return

        from . import telegram

        def run_bot():
            logging.basicConfig(level=logging.INFO)
            try:
                asyncio.run(start_bot())
            except KeyboardInterrupt:
                logging.info('Stopping bot...')

        async def start_bot():
            logging.info('Starting bot...')
            await telegram.dp.start_polling(telegram.bot)

        # Запускаем бота в отдельном процессе
        bot_process = multiprocessing.Process(target=run_bot, daemon=True)
        bot_process.start()
        self.bot_started = True