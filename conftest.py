import pytest
import requests
from utils.helpers import generate_unique_email


@pytest.fixture
def api_client():
    return requests.Session()


@pytest.fixture
def base_url():
    return "https://stellarburgers.education-services.ru/api"


@pytest.fixture
def user_data():
    return {
        "email": generate_unique_email(),
        "password": "password123",
        "name": "Test User"
    }


@pytest.fixture
def registered_user(api_client, base_url, user_data):
    response = api_client.post(f"{base_url}/auth/register", json=user_data)
    assert response.status_code == 200
    return user_data


@pytest.fixture
def auth_token(api_client, base_url, registered_user):
    response = api_client.post(f"{base_url}/auth/login", json={
        "email": registered_user["email"],
        "password": registered_user["password"]
    })
    assert response.status_code == 200
    token_data = response.json()
    return token_data["accessToken"]


@pytest.fixture
def ingredient_ids():
    return ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
