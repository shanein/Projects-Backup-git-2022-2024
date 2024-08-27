import sys

import pytest

sys.path.append("/app")
from main import app
from fastapi.testclient import TestClient
from uuid import UUID

client = TestClient(app)


@pytest.mark.usefixtures("get_user_sample")
def test_create_user(get_user_sample):
    userData = {
        "firstname": "hugo",
        "lastname": "bernard",
        "user_type": "advertiser",
    }
    userData = get_user_sample(userData)
    response = client.post("/auth/register", json=userData)
    response_data = response.json()
    assert response.status_code == 200
    try:
        uuid_obj = UUID(response_data["id"], version=4)
        assert str(uuid_obj) == response_data["id"]
    except ValueError:
        assert False, "L'ID n'est pas un UUID valide"


def test_login_user():
    sample_payload = {
        "email": "hugo.bernard@gmail.com",
        "password": "hugobernard",
    }
    response = client.post("/auth/login", json=sample_payload)
    response_data = response.json()
    assert response.status_code == 200
    try:
        uuid_obj = UUID(response_data["user"]["id"], version=4)
        assert str(uuid_obj) == response_data["user"]["id"]
    except ValueError:
        assert False, "L'ID n'est pas un UUID valide"


@pytest.mark.usefixtures("get_logged_user")
def test_delete_user(get_logged_user):
    advertiser = get_logged_user(
        {"email": "hugo.bernard@gmail.com", "password": "hugobernard"}
    )
    response = client.delete(f"/auth/delete/{advertiser['user']['id']}")
    assert response.status_code == 200
