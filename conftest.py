import pytest
import requests
from utils.helpers import generate_unique_email, generate_invalid_ingredient_hash
from utils.url import BASE_URL

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
def registered_user(api_client, user_data):
    resp = api_client.post(f"{BASE_URL}/auth/register", json=user_data)
    access_token = None
    try:
        if resp.status_code == 200:
            data = resp.json()
            access_token = data.get("accessToken")
    except Exception:
        access_token = None
    yield user_data
    token = access_token
    if not token:
       
        try:
            login_resp = api_client.post(f"{BASE_URL}/auth/login", json={
                "email": user_data["email"],
                "password": user_data["password"]
            })
            if login_resp.status_code == 200:
                token = login_resp.json().get("accessToken")
        except Exception:
            token = None
    if token:
    
        headers = {"Authorization": token}
        try:
            api_client.delete(f"{BASE_URL}/auth/user", headers=headers)
        except Exception:
            pass


@pytest.fixture
def auth_token(api_client, registered_user):
    resp = api_client.post(f"{BASE_URL}/auth/login", json={
        "email": registered_user["email"],
        "password": registered_user["password"]
    })

    if resp.status_code != 200:
        raise RuntimeError(f"Login failed in auth_token fixture: status {resp.status_code}")

    token_data = resp.json()
    token = token_data.get("accessToken")
    if not token:
        raise RuntimeError("No accessToken returned in auth_token fixture")

    return token

@pytest.fixture
def invalid_ingredient_hash():
    return ["invalid1", "not-a-real-id"]
