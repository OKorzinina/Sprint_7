
import requests
import allure
import pytest
from helps import CourierGenerator
from endpoints import CREATE_COURIER, LOGIN_COURIER, DELETE_COURIER

@allure.suite('API Курьер')
class TestCourierCreation:

    @allure.title('Успешное создание курьера')
    #@allure.description('Проверяем, что нового курьера можно создать с корректными данными')
    #def test_create_courier_success(self, register_and_delete_courier):
        #login = register_and_delete_courier['login']
        #password = register_and_delete_courier['password']

        #login_payload = {
            #"login": login,
            #"password": password
        #}
        #login_response = requests.post(LOGIN_COURIER, data=login_payload)

        #with allure.step('Проверка статуса ответа логина'):
            #assert login_response.status_code == 200
    @allure.title('Невозможно создать существующего курьера')
    @allure.description('Проверяем, что система не позволяет создать курьера с уже существующим логином.')
    def test_create_courier_success(self, register_and_delete_courier):
        login = register_and_delete_courier['login']
        password = register_and_delete_courier['password']
        first_name = register_and_delete_courier['firstName']

        # Попытка создать курьера с существующим логином и паролем.
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name  # Добавлен firstName для полноты данных
        }

        with allure.step('Попытка создать существующего курьера'):
            response = requests.post(CREATE_COURIER, data=payload)

        with allure.step('Проверка статуса ответа - должен быть конфликт (409)'):
            assert response.status_code == 409

        with allure.step('Проверка сообщения об ошибке'):
            assert response.json().get('message') == "Этот логин уже используется. Попробуйте другой."

#


    
        with allure.step('Проверка наличия ID в ответе логина'):
            assert 'id' in login_response.json()
            assert login_response.json().get('id') is not None

    @allure.title('Невозможно создать двух одинаковых курьеров')
    @allure.description('Проверяем, что система не позволяет создать курьера с уже существующим логином')
    def test_create_duplicate_courier_fails(self, register_and_delete_courier):
        login = register_and_delete_courier['login']
        password = register_and_delete_courier['password']

        with allure.step('Попытка создать курьера'):
            duplicate_payload = {
                "login": login,
                "password": password,
                "firstName": "new_name"
            }
            response = requests.post(CREATE_COURIER, data=duplicate_payload)

        with allure.step('Проверка статуса ответа на создание дубликата'):
            assert response.status_code == 409
        with allure.step('Проверка сообщения об ошибке'):
            assert response.json().get('message') == "Этот логин уже используется. Попробуйте другой."

    @allure.title('Для создания курьера необходимы все обязательные поля')
    @allure.description('Проверяем, что без обязательных полей login, password или firstName курьер не создается')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("payload", [
        {"password": "test_password", "firstName": "test_name"},  # Нет login
        {"login": "test_login", "firstName": "test_name"},      # Нет password
        {"login": "test_login", "password": "test_password"}   # Нет firstName
    ])
    def test_create_courier_missing_required_fields_fails(self, payload):
        generator = CourierGenerator()
        if "login" not in payload:
            payload["login"] = generator.generate_random_string(10)
        if "password" not in payload:
            payload["password"] = generator.generate_random_string(10)

        with allure.step(f'Попытка создать курьера с неполными данными: {payload}'):
            response = requests.post(CREATE_COURIER, data=payload)

        with allure.step('Проверка статуса ответа на неполные данные'):
            assert response.status_code == 400
        with allure.step('Проверка сообщения об ошибке'):
            assert response.json().get('message') == "Недостаточно данных для создания учетной записи"

    @allure.title('Успешный запрос создания курьера возвращает {"ok":true}')
    @allure.description('Проверяем содержание ответа при успешном создании курьера')
    def test_create_courier_returns_ok_true(self, register_and_delete_courier):
        generator = CourierGenerator()
        login = generator.generate_random_string(10)
        password = generator.generate_random_string(10)
        first_name = generator.generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(CREATE_COURIER, data=payload)

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 201
        with allure.step('Проверка тела ответа на {"ok":true}'):
            assert response.json() == {"ok": True}

        login_payload = {"login": login, "password": password}
        login_response = requests.post(LOGIN_COURIER, data=login_payload)
        if login_response.status_code == 200 and 'id' in login_response.json():
            courier_id = login_response.json()['id']
            requests.delete(f"{DELETE_COURIER}{courier_id}")

