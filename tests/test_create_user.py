import allure
import pytest


class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    @allure.description("Тест на успешное создание нового пользователя")
    def test_create_unique_user_success(self, api_client, base_url, user_data):
        with allure.step("Отправить запрос на создание пользователя"):
            response = api_client.post(f"{base_url}/auth/register", json=user_data)
        
        with allure.step("Проверить статус код и ответ"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "accessToken" in response_data
            assert "refreshToken" in response_data
            assert response_data["user"]["email"] == user_data["email"]
            assert response_data["user"]["name"] == user_data["name"]

    @allure.title("Создание уже зарегистрированного пользователя")
    @allure.description("Тест на попытку создания пользователя с существующим email")
    def test_create_existing_user_fail(self, api_client, base_url, registered_user):
        with allure.step("Попытаться создать пользователя с тем же email"):
            response = api_client.post(f"{base_url}/auth/register", json=registered_user)
        
        with allure.step("Проверить ошибку конфликта"):
            assert response.status_code == 403
            response_data = response.json()
            assert response_data["success"] is False
            assert "User already exists" in response_data["message"]

    @allure.title("Создание пользователя без обязательного поля")
    @allure.description("Тест на создание пользователя без пароля")
    def test_create_user_missing_required_field_fail(self, api_client, base_url, user_data):
        with allure.step("Создать данные пользователя без пароля"):
            incomplete_data = user_data.copy()
            del incomplete_data["password"]
        
        with allure.step("Отправить запрос с неполными данными"):
            response = api_client.post(f"{base_url}/auth/register", json=incomplete_data)
        
        with allure.step("Проверить ошибку валидации"):
            assert response.status_code == 403
            response_data = response.json()
            assert response_data["success"] is False
