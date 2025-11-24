import requests
import allure
import pytest
from helps import CourierGenerator
from endpoints import CREATE_COURIER, LOGIN_COURIER, DELETE_COURIER

@allure.suite('API Курьер')
class TestCourierCreation:

    @allure.title('Успешный логин курьера')
    @allure.description('Проверяем, что уже созданного курьера можно успешно залогинить')
    def test_login_courier_success(self, register_and_delete_courier):
        login = register_and_delete_courier['login']
        password = register_and_delete_courier['password']

        login_payload = {
            "login": login,
            "password": password
        }
        login_response = requests.post(LOGIN_COURIER, data=login_payload)

        with allure.step('Проверка статуса ответа логина'):
            assert login_response.status_code == 200
        with allure.step('Проверка наличия ID в ответе логина'):
            assert 'id' in login_response.json()
            assert login_response.json().get('id') is not None

    @allure.title('Невозможно создать двух одинаковых курьеров')
    @allure.description('Проверяем, что система не позволяет создать курьера с уже существующим логином')
    def test_create_duplicate_courier_fails(self, register_and_delete_courier):
        login = register_and_delete_courier['login']
        password = register_and_delete_courier['password']

        duplicate_payload = {
            "login": login,
            "password": password,
            "firstName": "new_name" 
        }
        with allure.step('Попытка создать курьера с уже существующим логином'):
            response = requests.post(CREATE_COURIER, data=duplicate_payload)

        with allure.step('Проверка статуса ответа на создание дубликата'):
            assert response.status_code == 409
        with allure.step('Проверка сообщения об ошибке'):
            assert response.json().get('message') == "Этот логин уже используется. Попробуйте другой."


    @allure.title('Для создания курьера необходимы все обязательные поля')
    @allure.description('Проверяем, что без обязательных полей login, password или firstName курьер не создается')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("missing_field", [
        "login",  # Нет login
        "password",  # Нет password
        "firstName"  # Нет firstName
    ])
    def test_create_courier_missing_required_fields_fails(self, missing_field):
        generator = CourierGenerator()
        base_payload = {
            "login": generator.generate_random_string(10),
            "password": generator.generate_random_string(10),
            "firstName": generator.generate_random_string(10)
        }
        test_payload = base_payload.copy()
        del test_payload[missing_field] # Удаляем требуемое поле

        with allure.step(f'Попытка создать курьера без поля "{missing_field}"'):
            response = requests.post(CREATE_COURIER, data=test_payload)

        with allure.step('Проверка статуса ответа на неполные данные'):
            assert response.status_code == 400
        with allure.step('Проверка сообщения об ошибке'):
            assert response.json().get('message') == "Недостаточно данных для создания учетной записи"


    @allure.title('Успешный запрос создания курьера возвращает {"ok":true}')
    @allure.description('Проверяем содержание ответа при успешном создании курьера')
    def test_create_courier_returns_ok_true(self, generate_courier_data_and_cleanup):
        
        login = generate_courier_data_and_cleanup['login']
        password = generate_courier_data_and_cleanup['password']
        first_name = generate_courier_data_and_cleanup['firstName']

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        with allure.step('Отправка запроса на создание курьера'):
            response = requests.post(CREATE_COURIER, data=payload)

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 201
        with allure.step('Проверка тела ответа на {"ok":true}'):
            assert response.json() == {"ok": True}





