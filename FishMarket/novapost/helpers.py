import time
import requests
import logging

from novapost.models import Warehouses, Cities


def response_request(api_url, params, retries=20):
    try:
        response = requests.post(api_url, json=params)
        response.raise_for_status()
        response_data = response.json()

        if response_data.get('success') and response_data.get('data', []):
            return response_data.get('data')
        elif response_data.get('success') and not response_data.get('data', []):
            logging.warning('Запрос успешный! Данных нет')
            return {}

        elif not response_data.get('success'):
            logging.error(f'Ошибка запроса! Попыток Осталось:{retries}', response_data)
            print('Ожидаем 120 секунд...')
            time.sleep(120)
            if retries > 0:
                return response_request(api_url, params, retries - 1)

    except requests.exceptions.Timeout:
        if retries > 0:
            logging.warning(f'Пробуем повторить запрос! Попыток осталось: {retries}')
            print('Ожидаем 120 секунд...')
            time.sleep(120)
            return response_request(api_url, params, retries - 1)
        else:
            logging.error('Тайм-Аут! Повторы для запроса исчерпаны')

    except requests.exceptions.ConnectionError as e:
        logging.error(f"Ошибка соединения: {e}")
        print('Ожидаем 120 секунд и повторим запрос')
        time.sleep(120)
        if retries > 0:
            return response_request(api_url, params, retries - 1)
        else:
            logging.error('Ошибка Соединения! Повторы для запроса исчерпаны')

    except requests.exceptions.RequestException as e:
        error_type = type(e).__name__
        logging.error(f"Ошибка запроса: Тип ошибки: {error_type} {e}")


def request_data_size(api_url, params):
    response = requests.post(api_url, json=params)
    response.raise_for_status()
    response_data = response.json()

    if response_data.get('success') and response_data.get('info').get('totalCount'):
        return response_data.get('info').get('totalCount')
    else:
        logging.error('Ошибка получения размера json data', response_data)
        raise ValueError('Ошибка request_data_size(), получен некорректный ответ')


def warehouse_object(warehouse):
    w = Warehouses(
            city=Cities.objects.get(ref_to_warehouses=warehouse["CityRef"]),
            number=warehouse["Number"],
            address_ua=warehouse["ShortAddress"].lower(),
            address_ru=warehouse["ShortAddressRu"].lower(),
            typeofwarehouse=2 if warehouse["TypeOfWarehouse"] == "f9316480-5f2d-425d-bc2c-ac7cd29decf0" else 1
        )
    return w


def delete_cities_and_warehouses():
    try:
        Cities.objects.all().delete()
        Warehouses.objects.all().delete()
    except Exception as e:
        logging.error(f'Ошибка при delete_cities_and_warehouses', e)

