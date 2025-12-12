import allure
import pytest
from utils.url import BASE_URL, ORDERS
from utils.ingredient import INGREDIENT_IDS
from utils.ingredient import INVALID_INGREDIENT_HASH


class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, api_client, auth_token):

        headers = {"Authorization": auth_token}
        order_data = {"ingredients": INGREDIENT_IDS}

        with allure.step("Создать заказ с авторизацией"):
            resp = api_client.post(BASE_URL + ORDERS, json=order_data, headers=headers)

        assert resp.status_code == 200
        assert resp.json().get("success") is True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, api_client, ingredients):

        order_data = {"ingredients": ingredients}
        resp = api_client.post(BASE_URL + ORDERS, json=order_data)

        assert resp.status_code == 401
        assert resp.json().get("message") == "You should be authorised"

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, api_client, auth_token):
        headers = {"Authorization": auth_token}

        resp = api_client.post(BASE_URL + ORDERS, json={}, headers=headers)

        assert resp.status_code == 400
        assert resp.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash_fail(self, api_client, auth_token):
        headers = {"Authorization": auth_token}
        resp = api_client.post(
            BASE_URL + ORDERS,
            json={"ingredients": INVALID_INGREDIENT_HASH},
            headers=headers
        )

        assert resp.status_code == 500 