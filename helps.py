
import requests
import random
import string
from endpoints import CREATE_COURIER

class CourierGenerator:
    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def register_new_courier_and_return_login_password(self):
        login_pass_name = []

        login = self.generate_random_string(10)
        password = self.generate_random_string(10)
        first_name = self.generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(CREATE_COURIER, data=payload)

        if response.status_code == 201:
            login_pass_name.append(login)
            login_pass_name.append(password)
            login_pass_name.append(first_name)
        return {"login": login, "password": password, "firstName": first_name}

