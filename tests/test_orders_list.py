
import requests
import allure
from endpoints import GET_ORDERS_LIST

@allure.suite('API Заказ')
class TestOrdersList:

    @allure.title('Получение списка заказов')
    @allure.description('Проверяем, что запрос списка заказов возвращает непустой список')
    def test_get_orders_list(self):
        with allure.step('Попытка получить список заказов'):
            response = requests.get(GET_ORDERS_LIST)

        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200
        with allure.step('Проверка, что тело ответа содержит ключ data и это список'):
            assert 'orders' in response.json()
            assert isinstance(response.json()['orders'], list)
        with allure.step('Проверка, что список заказов не пустой'):
            assert len(response.json()['orders']) >= 0



