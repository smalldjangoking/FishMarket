import time
from django.db import transaction
import math
from novapost.models import Cities, Warehouses
from django.conf import settings
from .helpers import response_request, request_data_size

NOVA_API = settings.NOVAPOST_API
api_url = "https://api.novaposhta.ua/v2.0/json/"


def save_cities_to_db():
    """Saves all cities (2 fields: name, ref_to_warehouses) to the database."""
    params = {
        "apiKey": f"{NOVA_API}",
        "modelName": "Address",
        "calledMethod": "getCities",
        "methodProperties": {
            "Limit": 1,
            "Page": 1
        }
    }

    total_number = request_data_size(api_url=api_url, params=params)
    print('Записей на добавление:', total_number)
    print('Устанавливаем лимиты Загрузка перед началом скачивания 120 секунд...')
    time.sleep(120)
    limit = params['methodProperties']['Limit'] = 500
    iterations = math.ceil(total_number / limit)

    with transaction.atomic():
        for page in range(1, iterations + 1):
            params["methodProperties"]["Page"] = page
            print('Обработка страницы', page)
            cities = response_request(api_url=api_url, params=params)

            if cities:
                city_objects = [
                    Cities(
                        city_name=city_data['Description'] + f" ({city_data['AreaDescription']} обл.)"
                        if '(' not in city_data['Description']
                        else city_data['Description'],
                        ref_to_warehouses=city_data['Ref']
                    )
                    for city_data in cities
                ]
                Cities.objects.bulk_create(city_objects)




def save_warehouses_to_db():
    """Saves all warehouses (3 fields: city, address, type of warehouse) to the database."""
    params = {
        "apiKey": f"{NOVA_API}",
        "modelName": "Address",
        "calledMethod": "getWarehouses",
        "methodProperties": {
            "Limit": 1,
            "Page": 1
        }
    }

    total_number = request_data_size(api_url=api_url, params=params)
    limit = params['methodProperties']['Limit'] = 500
    iterations = math.ceil(total_number / limit)
    print('Записей на добавление:', total_number)
    print('Устанавливаем лимиты... Загрузка перед началом скачивания 120 секунд...')
    time.sleep(120)

    with transaction.atomic():
        for page in range(1, iterations + 1):
            print('Обработка страницы', page)
            params["methodProperties"]["Page"] = page

            warehouses = response_request(api_url=api_url, params=params)

            if warehouses:
                warehouse_objects = [
                    Warehouses(
                        city=Cities.objects.get(ref_to_warehouses=warehouse['CityRef']),
                        address=(
                            f"Від. №{warehouse['Number']} - {warehouse['ShortAddress']}"
                            if warehouse['TypeOfWarehouse'] != 'f9316480-5f2d-425d-bc2c-ac7cd29decf0'
                            else f"Поштомат №{warehouse['Number']} - {warehouse['ShortAddress']}"
                        ),
                        typeofwarehouse=(1 if warehouse['TypeOfWarehouse'] != 'f9316480-5f2d-425d-bc2c-ac7cd29decf0' else 2)
                    )
                for warehouse in warehouses
                ]

                Warehouses.objects.bulk_create(warehouse_objects)
