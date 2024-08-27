import pytest
import sys

sys.path.append("/app")
from main import app
from fastapi.testclient import TestClient
from schemas.userSchema import UserCreate

client = TestClient(app)


@pytest.fixture(scope="module")
def get_user_sample():
    def _get_user_sample(userData):
        sample_user = {
            "firstname": userData["firstname"],
            "lastname": userData["lastname"],
            "email": userData["firstname"] + "." + userData["lastname"] + "@gmail.com",
            "password": userData["firstname"] + userData["lastname"],
            "birthdate": "2023-03-17",
            "phone_number": "0606060606",
            "company_name": "Doe & Co",
            "user_type": userData["user_type"],
        }
        return sample_user

    return _get_user_sample


@pytest.fixture(scope="module")
def get_logged_user():
    def _get_logged_user(userData):
        sample_payload = {
            "email": userData["email"],
            "password": userData["password"],
        }
        return client.post("/auth/login", json=sample_payload).json()

    return _get_logged_user
