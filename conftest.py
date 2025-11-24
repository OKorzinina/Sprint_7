
#import pytest
#import requests
#from helps import CourierGenerator
#from endpoints import CREATE_COURIER, LOGIN_COURIER, DELETE_COURIER

#@pytest.fixture(scope="function")
#def register_and_delete_courier():
    #generator = CourierGenerator()
    #courier_data = generator.register_new_courier_and_return_login_password()
    #login = courier_data['login']
    #password = courier_data['password']
    #first_name = courier_data['firstName']

    #yield courier_data

    #login_payload = {
        #"login": login,
        #"password": password
    #}
    #login_response = requests.post(LOGIN_COURIER, data=login_payload)

    #if login_response.status_code == 200:
        #courier_id = login_response.json().get("id")
        #if courier_id:
            #delete_url = f"{DELETE_COURIER}{courier_id}"
           # delete_response = requests.delete(delete_url)
            #if delete_response.status_code == 200:
                #print(f"\nКурьер с ID {courier_id} успешно удален.")
            #else:
                #print(f"\nНе удалось удалить курьера с ID {courier_id}. Статус: {delete_response.status_code}, Ответ: {delete_response.text}")
        #else:
            #print(f"\nID курьера не найден после логина для удаления.")
    #else:
        #print(f"\nНе удалось залогиниться для получения ID курьера {login} для удаления.")

import pytest
import requests
from helps import CourierGenerator
from endpoints import CREATE_COURIER, LOGIN_COURIER, DELETE_COURIER
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.fixture(scope="function")
def register_and_delete_courier():
    generator = CourierGenerator()
    courier_data = generator.register_new_courier_and_return_login_password()
    login = courier_data['login']
    password = courier_data['password']

    yield courier_data

    
    login_payload = {
        "login": login,
        "password": password
    }

    login_response = requests.post(LOGIN_COURIER, data=login_payload)

    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
        if courier_id:
            delete_url = f"{DELETE_COURIER}{courier_id}"
            delete_response = requests.delete(delete_url)
            if delete_response.status_code == 200:
                logging.info(f"Курьер с ID {courier_id} успешно удален (из register_and_delete_courier).")
            else:
                logging.error(f"Не удалось удалить курьера с ID {courier_id} (из register_and_delete_courier). Статус: {delete_response.status_code}, Ответ: {delete_response.text}")
        else:
            logging.warning(f"ID курьера не найден после логина для удаления курьера: {login}.")
    else:
        logging.arning(f"Не удалось залогиниться для получения ID курьера {login} для удаления (из register_and_delete_courier). Статус: {login_response.status_code}, Ответ: {login_response.text}")


@pytest.fixture(scope="function")
def generate_courier_data_and_cleanup():
    """
    Фикстура, которая генерирует данные для курьера и возвращает их.
    После теста, если курьер был создан, она его удаляет.
    """
    generator = CourierGenerator()
    login = generator.generate_random_string(10)
    password = generator.generate_random_string(10)
    first_name = generator.generate_random_string(10)

    courier_to_cleanup = {'login': login, 'password': password, 'firstName': first_name}

    yield courier_to_cleanup 

    
    login_payload = {
        "login": login,
        "password": password
    }

    login_response = requests.post(LOGIN_COURIER, data=login_payload)
    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
        if courier_id:
            delete_url = f"{DELETE_COURIER}{courier_id}"
            delete_response = requests.delete(delete_url)
            if delete_response.status_code == 200:
                logging.info(f"Курьер с ID {courier_id} (созданный в тесте) успешно удален во время cleanup.")
            else:
                logging.error(f"Не удалось удалить курьера с ID {courier_id} (созданный в тесте). Статус: {delete_response.status_code}, Ответ: {delete_response.text}")
        else:
            logging.warning(f"ID курьера для cleanup не найден после логина для {login}.")
    else:
        logging.info(f"Курьер {login} не был найден для удаления (возможно, не был создан успешно). Статус: {login_response.status_code}, Ответ: {login_response.text}")






