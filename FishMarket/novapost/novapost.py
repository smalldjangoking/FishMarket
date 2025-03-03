import logging
import time
from django.db import transaction
import math
from novapost.models import Cities, Warehouses
from django.conf import settings
from .helpers import response_request, request_data_size, warehouse_object

NOVA_API = settings.NOVAPOST_API
api_url = "https://api.novaposhta.ua/v2.0/json/"


def save_cities_to_db(one_city=False):
    """Saves all cities (3 fields: city_name, city_state, ref_to_warehouses) to the database."""
    params = {
        "apiKey": f"{NOVA_API}",
        "modelName": "Address",
        "calledMethod": "getCities",
        "methodProperties": {
            "Limit": 1,
            "Page": 1
        }
    }

    if one_city:
        params['methodProperties'] = {"Ref": f"{one_city}"}
        iterations = 1

    else:
        total_number = request_data_size(api_url=api_url, params=params)
        print('Записей на добавление:', total_number)
        print('Ожидание 120 секунд.')
        time.sleep(120)
        limit = params['methodProperties']['Limit'] = 500
        iterations = math.ceil(total_number / limit)

    for page in range(1, iterations + 1):
        params["methodProperties"]["Page"] = page
        print('Обработка страницы', page)
        cities = response_request(api_url=api_url, params=params)
        if cities:
            try:
                city_objects = [
                    Cities(
                        city_name_ua=city_data['Description'].split('(')[0].lower() if '(' in city_data[
                            'Description'] else
                        city_data['Description'].lower(),
                        city_name_ru=city_data['DescriptionRu'].split('(')[0].lower() if '(' in city_data[
                            'DescriptionRu'] else
                        city_data['DescriptionRu'].lower(),
                        city_state=f"{city_data['SettlementTypeDescription']}, {city_data['Description'].split('(')[1]}"
                        if '(' in city_data['Description']
                        else f"{city_data['SettlementTypeDescription']}, {city_data['AreaDescription']} обл.",
                        ref_to_warehouses=city_data['Ref']
                    )
                    for city_data in cities
                ]
                Cities.objects.bulk_create(city_objects)

            except Exception as e:
                logging.error(f'Ошибка при обработке городов в базу. save_cities_to_db()', e)

    return True


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
    print('ожидание 120 секунд')
    time.sleep(120)

    for page in range(1, iterations + 1):
        print('Обработка страницы', page)
        params["methodProperties"]["Page"] = page

        warehouses = response_request(api_url=api_url, params=params)

        if warehouses:
            warehouse_objects = []
            for warehouse in warehouses:
                try:
                    warehouse_objects.append(warehouse_object(warehouse))
                except Cities.DoesNotExist:
                    print(f"Город с ref_to_warehouses={warehouse} не найден в таблице Cities.")
                    print('____________________________________________________________')
                    one_city = save_cities_to_db(warehouse['CityRef'])

                    if one_city:
                        print('Город успешно добавлен!')
                        warehouse_objects.append(warehouse_object(warehouse))
                        print('В базу добавлен warehouse после создания города.')

                except Exception as e:
                    logging.error(f'Ошибка при обработке почтовых отделений в базу. save_warehouses_to_db()', e)


            Warehouses.objects.bulk_create(warehouse_objects)
