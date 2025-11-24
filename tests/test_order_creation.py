
import requests
import allure
import json
import pytest
from endpoints import CREATE_ORDER

@allure.suite('API Заказ')
class TestOrderCreation:

    @allure.title('Успешное создание заказа с различными параметрами цвета')
    @allure.description('Проверяем, что заказ может быть успешно создан с указанием одного цвета, обоих цветов или без цвета')
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_colors(self, color):
        payload = {
            "firstName": "Иван",
            "lastName": "Иванов",
            "address": "Москва, ул. Пушкина, 10",
            "metroStation": 4,
            "phone": "+7 999 123 45 67",
            "rentTime": 5,
            "deliveryDate": "2024-12-31",
            "comment": "Тестовый заказ",
            "color": color
        }

        with allure.step(f'Попытка создать заказ с цветом: {color}'):
            response = requests.post(CREATE_ORDER, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 201
        with allure.step('Проверка наличия track в теле ответа'):
            assert 'track' in response.json()
            assert response.json()['track'] is not None

