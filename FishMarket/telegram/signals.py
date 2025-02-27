import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from checkout.models import Order
from telegram.tasks import send_telegram_notification

@receiver(post_save, sender=Order)
def notify_new_order(sender, instance, created, **kwargs):
    """Перехватываем сохранение в базу, для оповещения бота в телеграм. Next CeleryWorker"""
    if created:
        send_telegram_notification.delay(instance.id)
        logging.info(f"Telegram notification task queued for order {instance.id}")
