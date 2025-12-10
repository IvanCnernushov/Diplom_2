import allure
import pytest
from utils.url import BASE_URL


class TestLoginUser:
    @allure.title("Успешный вход существующего пользователя")
    def test_login_existing_user_success(self, api_client, user_data):

        reg = api_client.post(f"{BASE_URL}/auth/register", json=user_data)
        assert reg.status_code == 200

        with allure.step("Выполнить login"):
            response = api_client.post(f"{BASE_URL}/auth/login", json={
                "email": user_data["email"],
                "password": user_data["password"]
            })

        with allure.step("Проверить ответ"):
            assert response.status_code == 200
            data = response.json()
            assert "accessToken" in data

    @allure.title("Вход с неверным логином/паролем")
    @pytest.mark.parametrize("bad_creds", [
        ({"email": "notexists@example.com", "password": "whatever"}),
        ({"email": "wrong@example.com", "password": "wrongpass"}),
    ])
    def test_login_with_invalid_credentials(self, api_client, bad_creds):
        response = api_client.post(f"{BASE_URL}/auth/login", json=bad_creds)
        
        assert response.status_code in (401, 403)
        data = response.json()
        assert data.get("success") is False
