import allure
import pytest


class TestLoginUser:
    @allure.title("Успешный вход существующего пользователя")
    @allure.description("Тест на успешную авторизацию зарегистрированного пользователя")
    def test_login_existing_user_success(self, api_client, base_url, registered_user):
        with allure.step("Отправить запрос на авторизацию"):
            response = api_client.post(f"{base_url}/auth/login", json={
                "email": registered_user["email"],
                "password": registered_user["password"]
            })

        with allure.step("Проверить успешную авторизацию"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "accessToken" in response_data
            assert "refreshToken" in response_data
            assert response_data["user"]["email"] == registered_user["email"]

    @allure.title("Вход с неверными учетными данными")
    @allure.description("Тест на попытку входа с неправильным email и паролем")
    def test_login_with_invalid_credentials_fail(self, api_client, base_url):
        with allure.step("Отправить запрос с неверными данными"):
            response = api_client.post(f"{base_url}/auth/login", json={
                "email": "nonexistent@example.com",
                "password": "wrongpassword"
            })

        with allure.step("Проверить ошибку авторизации"):
            assert response.status_code == 401
            response_data = response.json()
            assert response_data["success"] is False
            assert "email or password are incorrect" in response_data["message"]
