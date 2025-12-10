import allure
import pytest
from utils.url import BASE_URL
from utils.ingredient import INGREDIENT_IDS


class TestCreateOrder:
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, api_client, registered_user):
        
        login = api_client.post(f"{BASE_URL}/auth/login", json={
            "email": registered_user["email"],
            "password": registered_user["password"]
        })
        assert login.status_code == 200
        token = login.json().get("accessToken")

        headers = {"Authorization": token}
        order_data = {"ingredients": INGREDIENT_IDS}

        with allure.step("Создать заказ с авторизацией"):
            resp = api_client.post(f"{BASE_URL}/orders", json=order_data, headers=headers)

        assert resp.status_code == 200
        assert resp.json().get("success") is True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, api_client):
        order_data = {"ingredients": INGREDIENT_IDS}
        resp = api_client.post(f"{BASE_URL}/orders", json=order_data)
        
        assert resp.status_code in (401, 403, 200)

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, api_client):
        resp = api_client.post(f"{BASE_URL}/orders", json={})
        
        assert resp.status_code in (400, 403)

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash_fail(self, api_client, invalid_ingredient_hash):
        order_data = {"ingredients": [invalid_ingredient_hash]}
        resp = api_client.post(f"{BASE_URL}/orders", json=order_data)
        
        assert resp.status_code in (400, 500, 403)
