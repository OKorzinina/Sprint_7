
import requests
import allure
import pytest
from helps import CourierGenerator
from endpoints import CREATE_COURIER, LOGIN_COURIER, DELETE_COURIER

@allure.suite('API Курьер')
class TestCourierLogin:

    @allure.title('Успешный логин курьера')
    @allure.description('Проверяем, что зарегистрированный курьер может успешно авторизоваться')
    def test_courier_login_success(self, register_and_delete_courier):
        login = register_and_delete_courier['login']
        password = register_and_delete_courier['password']

        login_payload = {
            "login": login,
            "password": password
        }

        with allure.step('Попытка логина курьера'):
            response = requests.post(LOGIN_COURIER, data=login_payload)

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200
        with allure.step('Проверка наличия ID в ответе'):
            assert 'id' in response.json()
            assert response.json().get('id') is not None

    @allure.title('Логин курьера с неправильным логином')
    @allure.description('Проверяем, что при логине с несуществующим логином возвращается ошибка')
    def test_courier_login_wrong_login_fails(self, register_and_delete_courier):
        password = register_and_delete_courier['password']

        login_payload = {
            "login": "not_existing_login",
            "password": password
        }

        with allure.step('Попытка логина с несуществующим логином'):
            response = requests.post(LOGIN_COURIER, data=login_payload)

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404
        with allure.step('Проверка сообщения об ошибке'):
            assert response.json().get('message') == "Учетная запись не найдена"

    @allure.title('Логин курьера с неправильным паролем')
    @allure.description('Проверяем, что при логине с неправильным паролем возвращается ошибка')
    def test_courier_login_wrong_password_fails(self, register_and_delete_courier):
        login = register_and_delete_courier['login']

        login_payload = {
            "login": login,
            "password": "wrong_password"
        }

        with allure.step('Попытка логина с неправильным паролем'):
            response = requests.post(LOGIN_COURIER, data=login_payload)

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404
        with allure.step('Проверка сообщения об ошибке'):
            assert response.json().get('message') == "Учетная запись не найдена"

    @allure.title('Логин курьера без обязательных полей')
    @allure.description('Проверяем, что при логине без логина или пароля возвращается ошибка')
    @pytest.mark.parametrize("payload", [
        {"password": "test_password"},  # Нет логина
        {"login": "test_login"}          # Нет пароля
    ])
    def test_courier_login_missing_required_fields_fails(self, payload):
        with allure.step(f'Попытка логина с неполными данными: {payload}'):
            response = requests.post(LOGIN_COURIER, data=payload)

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 400
        with allure.step('Проверка сообщения об ошибке'):
            assert response.json().get('message') == "Недостаточно данных для входа"

