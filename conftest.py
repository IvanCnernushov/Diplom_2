import pytest
import requests
from utils.helpers import generate_unique_email
from utils.url import BASE_URL, REGISTER, LOGIN, USER, INGREDIENTS


@pytest.fixture
def api_client():
    sess = requests.Session()
    yield sess
    sess.close()


@pytest.fixture
def user_data():
    return {
        "email": generate_unique_email(),
        "password": "password123",
        "name": "Test User"
    }


@pytest.fixture
def create_user(api_client):
    def _create(payload):
        return api_client.post(BASE_URL + REGISTER, json=payload)
    return _create


@pytest.fixture
def login_user(api_client):
    def _login(email, password):
        return api_client.post(
            BASE_URL + LOGIN,
            json={"email": email, "password": password}
        )
    return _login


@pytest.fixture
def registered_user(create_user, login_user, api_client, user_data):

    create_user(user_data)
    login_response = login_user(user_data["email"], user_data["password"])
    token = login_response.json().get("accessToken")

    yield {
        "email": user_data["email"],
        "password": user_data["password"],
        "token": token,
        "data": user_data
    }

    if token:
        api_client.delete(
            BASE_URL + USER,
            headers={"Authorization": token}
        )


@pytest.fixture
def auth_token(login_user, registered_user):
    token = registered_user.get("token")
    return token


@pytest.fixture
def ingredients(api_client):
    resp = api_client.get(BASE_URL + INGREDIENTS)
    data = resp.json().get("data", [])
    return [data[0]["_id"], data[1]["_id"]]

