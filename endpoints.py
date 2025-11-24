
from urls import BASE_URL

# Эндпоинты для курьеров
CREATE_COURIER = f"{BASE_URL}/api/v1/courier"
LOGIN_COURIER = f"{BASE_URL}/api/v1/courier/login"
DELETE_COURIER = f"{BASE_URL}/api/v1/courier/"  # ID курьера будет добавляться после

# Эндпоинты для заказов
CREATE_ORDER = f"{BASE_URL}/api/v1/orders"
GET_ORDERS_LIST = f"{BASE_URL}/api/v1/orders"

