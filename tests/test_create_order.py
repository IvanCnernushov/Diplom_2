import allure
import pytest
from utils.helpers import generate_invalid_ingredient_hash


class TestCreateOrder:

    @allure.title("Создание заказа без авторизации")
    @allure.description("Проверка успешного создания заказа без авторизации")
    def test_create_order_without_auth_success(self, api_client, base_url, ingredient_ids):
        with allure.step("Создать данные заказа с валидными ингредиентами"):
            order_data = {
                "ingredients": ingredient_ids
            }

        with allure.step("Отправить запрос без авторизации"):
            response = api_client.post(f"{base_url}/orders", json=order_data)

        with allure.step("Проверить успешное создание заказа"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "order" in response_data
            assert "number" in response_data["order"]
            assert "name" in response_data

    @allure.title("Создание заказа с авторизацией")
    @allure.description("Проверка успешного создания заказа с авторизацией")
    def test_create_order_with_auth_success(self, api_client, base_url, auth_token, ingredient_ids):
        with allure.step("Подготовить заголовок с авторизацией"):
            headers = {"Authorization": auth_token}

        with allure.step("Создать данные заказа"):
            order_data = {
                "ingredients": ingredient_ids
            }

        with allure.step("Отправить запрос с авторизацией"):
            response = api_client.post(f"{base_url}/orders", json=order_data, headers=headers)

        with allure.step("Проверить успешное создание заказа"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "order" in response_data
            assert "number" in response_data["order"]

    @allure.title("Создание заказа без ингредиентов - ошибка валидации")
    @allure.description("Проверка, что API возвращает ошибку при пустом списке ингредиентов")
    def test_create_order_without_ingredients_fail(self, api_client, base_url):
        with allure.step("Создать заказ без ингредиентов"):
            order_data = {
                "ingredients": []
            }

        with allure.step("Отправить запрос на создание заказа"):
            response = api_client.post(f"{base_url}/orders", json=order_data)

        with allure.step("Проверить ошибку валидации"):
            assert response.status_code == 400
            response_data = response.json()
            assert response_data["success"] is False
            assert "message" in response_data
            assert "Ingredient ids must be provided" in response_data["message"]

    @allure.title("Создание заказа с неверным хешем ингредиентов - внутренняя ошибка сервера")
    @allure.description("API возвращает 500 при невалидных ID ингредиентов")
    def test_create_order_with_invalid_ingredient_hash_fail(self, api_client, base_url):
        with allure.step("Создать заказ с невалидными ингредиентами"):
            order_data = {
                "ingredients": [generate_invalid_ingredient_hash()]
            }

        with allure.step("Отправить запрос на создание заказа"):
            response = api_client.post(f"{base_url}/orders", json=order_data)

        with allure.step("Проверить внутреннюю ошибку сервера"):
            assert response.status_code == 500
