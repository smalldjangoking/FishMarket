import logging

from celery import shared_task
from django.db import transaction

from novapost.helpers import delete_cities_and_warehouses
from novapost.novapost import save_cities_to_db, save_warehouses_to_db


@shared_task
def novaposhta_api_initialization():
    """Function to initialize NovaPoshta API (Cities, Warehouses addresses to DB"""
    try:
        with transaction.atomic():
            # First step
            delete_cities_and_warehouses()

            # Second step
            save_cities_to_db()

            # Third step
            save_warehouses_to_db()

    except Exception as e:
        logging.error(f'Ошибка инициализации. novaposhta_api_initialization()', e)

    print('DONE!')
