import allure
import pytest
from utils.url import BASE_URL


class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    @allure.description("Тест на успешное создание нового пользователя")
    def test_create_unique_user_success(self, api_client, user_data):
        with allure.step("Отправить запрос на создание пользователя"):
            response = api_client.post(f"{BASE_URL}/auth/register", json=user_data)
        
        with allure.step("Проверить статус код и ответ"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data.get("success") is True
            assert "accessToken" in response_data


    @allure.title("Создание пользователя который уже зарегистрирован")
    @allure.description("Тест на повторную регистрацию")
    def test_create_user_already_registered(self, api_client, user_data):
       
        first = api_client.post(f"{BASE_URL}/auth/register", json=user_data)
        assert first.status_code == 200

        second = api_client.post(f"{BASE_URL}/auth/register", json=user_data)
        
        assert second.status_code in (403, 409)
        response_data = second.json()
        
        assert any(word in response_data.get("message", "").lower() for word in ["user", "already", "exist", "exists"])


    @allure.title("Создание пользователя без обязательного поля (параметризация)")
    @allure.description("Тест на создание пользователя без одного из обязательных полей")
    @pytest.mark.parametrize("missing_field, expected_substring", [
        ("email", "email"),
        ("password", "password"),
        ("name", "name"),
    ])
    def test_create_user_missing_required_field_fail(self, api_client, user_data, missing_field, expected_substring):
        with allure.step("Подготовить данные с пропуском обязательного поля"):
            incomplete = user_data.copy()
            incomplete.pop(missing_field, None)

        with allure.step("Отправить запрос с неполными данными"):
            response = api_client.post(f"{BASE_URL}/auth/register", json=incomplete)

        with allure.step("Проверить ошибку валидации"):
        
            assert response.status_code == 403
            response_data = response.json()
            assert response_data.get("success") is False
            assert expected_substring.lower() in response_data.get("message", "").lower()
