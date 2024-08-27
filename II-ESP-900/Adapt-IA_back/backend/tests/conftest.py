import sys

sys.path.append("/app")
from main import app
from fastapi.testclient import TestClient
from fixtures.user import *
from fixtures.campaign import *
from fixtures.terminal import *

client = TestClient(app)


def pytest_sessionstart(session):
    # Create advertiser for tests (except Create/delete user tests)
    advertiserData = {
        "firstname": "John",
        "lastname": "Doe",
        "email": "john@doe.com",
        "password": "johndoe",
        "birthdate": "2023-03-17",
        "phone_number": "0606060606",
        "company_name": "Doe & Co",
        "user_type": "advertiser",
    }
    client.post("/auth/register", json=advertiserData)

    # Create distributor for tests (except Create/delete user tests)
    distributorData = {
        "firstname": "Jane",
        "lastname": "Doe",
        "email": "jane@doe.com",
        "password": "janedoe",
        "birthdate": "2000-01-01",
        "phone_number": "0606060606",
        "company_name": "Doe & Co",
        "user_type": "distributor",
    }
    client.post("/auth/register", json=distributorData)


def pytest_sessionfinish(session, exitstatus):
    # Delete advertiser
    advertiserData = {
        "email": "john@doe.com",
        "password": "johndoe",
    }
    globalAdvertiser = client.post("/auth/login", json=advertiserData).json()
    client.delete(f"/auth/delete/{globalAdvertiser['user']['id']}")

    # Delete distributor
    distributorData = {
        "email": "jane@doe.com",
        "password": "janedoe",
    }
    globalDistributor = client.post("/auth/login", json=distributorData).json()
    client.delete(f"/auth/delete/{globalDistributor['user']['id']}")
