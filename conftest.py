
import pytest
import requests
from helps import CourierGenerator
from endpoints import CREATE_COURIER, LOGIN_COURIER, DELETE_COURIER

@pytest.fixture(scope="function")
def register_and_delete_courier():
    generator = CourierGenerator()
    courier_data = generator.register_new_courier_and_return_login_password()
    login = courier_data['login']
    password = courier_data['password']
    first_name = courier_data['firstName']

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
                print(f"\nКурьер с ID {courier_id} успешно удален.")
            else:
                print(f"\nНе удалось удалить курьера с ID {courier_id}. Статус: {delete_response.status_code}, Ответ: {delete_response.text}")
        else:
            print(f"\nID курьера не найден после логина для удаления.")
    else:
        print(f"\nНе удалось залогиниться для получения ID курьера {login} для удаления.")

