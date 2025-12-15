import allure
import pytest
from utils.url import BASE_URL, REGISTER


class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    @allure.description("Тест на успешное создание нового пользователя")
    def test_create_unique_user_success(self, api_client, user_data):
        response = api_client.post(BASE_URL + REGISTER, json=user_data)

        assert response.status_code == 200
        data = response.json()
        assert data.get("success") is True
        assert "accessToken" in data

    @allure.title("Создание пользователя который уже зарегистрирован")
    @allure.description("Тест на повторную регистрацию")
    def test_create_user_already_registered(self, api_client, registered_user):
 
        payload = registered_user["data"]

        response = api_client.post(BASE_URL + REGISTER, json=payload)

        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"

    @allure.title("Создание пользователя без обязательного поля")
    @allure.description("Проверка валидации обязательных полей через параметризацию")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field_fail(self, api_client, user_data, missing_field):
    
        incomplete = user_data.copy()
        incomplete.pop(missing_field)

        response = api_client.post(BASE_URL + REGISTER, json=incomplete)

        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"
