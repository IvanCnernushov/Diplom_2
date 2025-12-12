import allure
import pytest
from utils.url import BASE_URL, REGISTER, LOGIN


class TestLoginUser:

    @allure.title("Успешный вход существующего пользователя")
    def test_login_existing_user_success(self, api_client, registered_user):
  
        data = registered_user["data"]

        response = api_client.post(
            BASE_URL + LOGIN,
            json={"email": data["email"], "password": data["password"]}
        )

        assert response.status_code == 200
        assert "accessToken" in response.json()

    @allure.title("Вход с неверным логином/паролем")
    @pytest.mark.parametrize("bad_creds", [
        {"email": "notexists@example.com", "password": "whatever"},
        {"email": "wrong@example.com", "password": "wrongpass"},
    ])
    def test_login_with_invalid_credentials(self, api_client, bad_creds):

        response = api_client.post(BASE_URL + LOGIN, json=bad_creds)

        assert response.status_code == 401
        assert response.json()["message"] == "email or password are incorrect"
