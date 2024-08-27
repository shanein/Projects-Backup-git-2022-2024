import sys
import uuid

import pytest

sys.path.append("/app")

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

campaign_id = None


@pytest.mark.usefixtures("get_logged_user", "get_campaign_sample")
def test_create_campaign(get_logged_user, get_campaign_sample):
    return
    global campaign_id
    user = get_logged_user({"email": "john@doe.com", "password": "johndoe"})
    # Test with good data
    good_data = get_campaign_sample()
    response = client.post(
        "/campaigns/",
        json=good_data,
        headers={"Authorization": "Bearer " + user["token"]},
    )
    assert response.status_code == 200
    campaign_id = response.json()["id"]
    # Test with bad data
    response = client.post(
        "/campaigns/",
        json={},
        headers={"Authorization": "Bearer " + user["token"]},
    )
    print(response.json())
    assert response.status_code == 422
    # Test with not advertiser id
    response = client.post("/campaigns/", json=good_data)
    assert response.status_code == 401


@pytest.mark.usefixtures("get_logged_user")
def test_get_campaign(get_logged_user):
    return
    global campaign_id
    user = get_logged_user({"email": "john@doe.com", "password": "johndoe"})
    # Test with existant id
    response = client.get(
        f"/campaigns/{campaign_id}",
        headers={"Authorization": "Bearer " + user["token"]},
    )
    assert response.status_code == 200
    # Test with inexistant id
    false_id = uuid.uuid4()
    response = client.get(
        f"/campaigns/{false_id}", headers={"Authorization": "Bearer " + user["token"]}
    )
    assert response.status_code == 404
    # Test with not user id
    response = client.get(f"/campaigns/{campaign_id}")
    assert response.status_code == 401


@pytest.mark.usefixtures("get_logged_user")
def test_delete_campaign(get_logged_user):
    return
    global campaign_id
    user = get_logged_user({"email": "john@doe.com", "password": "johndoe"})
    # Test with existant id
    response = client.delete(
        f"/campaigns/{campaign_id}",
        headers={"Authorization": "Bearer " + user["token"]},
    )
    assert response.status_code == 200
    # Test with inexistant id
    false_id = uuid.uuid4()
    response = client.delete(
        f"/campaigns/{false_id}", headers={"Authorization": "Bearer " + user["token"]}
    )
    assert response.status_code == 404
    # Test with not creator id
    response = client.delete(f"/campaigns/{campaign_id}")
    assert response.status_code == 401
