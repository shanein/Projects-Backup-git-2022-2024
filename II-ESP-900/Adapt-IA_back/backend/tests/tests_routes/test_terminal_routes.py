import sys
import uuid

import pytest

sys.path.append("/app")

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

terminal_id = None


@pytest.mark.usefixtures("get_logged_user", "get_terminal_sample")
def test_create_terminal(get_logged_user, get_terminal_sample):
    global terminal_id
    user = get_logged_user({"email": "jane@doe.com", "password": "janedoe"})
    # Test with good data
    good_data = get_terminal_sample()
    response = client.post(
        "/terminal/",
        json=good_data,
        headers={"Authorization": "Bearer " + user["token"]},
    )
    assert response.status_code == 200
    terminal_id = response.json()["id"]
    # Test with bad data
    response = client.post(
        "/terminal/",
        json={},
        headers={"Authorization": "Bearer " + user["token"]},
    )
    assert response.status_code == 422
    # Test with not distributor id
    response = client.post("/terminal/", json=good_data)
    assert response.status_code == 401


@pytest.mark.usefixtures("get_logged_user")
def test_get_all_terminals(get_logged_user):
    user = get_logged_user({"email": "jane@doe.com", "password": "janedoe"})
    response = client.get(
        f"/terminal/", headers={"Authorization": "Bearer " + user["token"]}
    )
    assert response.status_code == 200


@pytest.mark.usefixtures("get_logged_user")
def test_get_terminal(get_logged_user):
    global terminal_id
    user = get_logged_user({"email": "jane@doe.com", "password": "janedoe"})
    # Test with existant id
    response = client.get(
        f"/terminal/{terminal_id}", headers={"Authorization": "Bearer " + user["token"]}
    )
    assert response.status_code == 200
    # Test with inexistant id
    false_id = uuid.uuid4()
    response = client.get(
        f"/terminal/{false_id}", headers={"Authorization": "Bearer " + user["token"]}
    )
    assert response.status_code == 404
    # Test with not user id
    response = client.get(f"/terminal/{terminal_id}")
    assert response.status_code == 401


@pytest.mark.usefixtures("get_logged_user")
def test_get_terminal_availability(get_logged_user):
    global terminal_id
    user = get_logged_user({"email": "jane@doe.com", "password": "janedoe"})
    response = client.get(
        f"/terminal/{terminal_id}/availability",
        headers={"Authorization": "Bearer " + user["token"]},
    )
    assert response.status_code == 200


@pytest.mark.usefixtures("get_logged_user")
def test_add_unavailability_period(get_logged_user):
    global terminal_id
    user = get_logged_user({"email": "jane@doe.com", "password": "janedoe"})
    # Test with good data
    new_period = {"start_date": "2023-12-24", "end_date": "2023-12-26"}
    response = client.post(
        f"/terminal/{terminal_id}/availability",
        headers={"Authorization": "Bearer " + user["token"]},
        json=new_period,
    )
    assert response.status_code == 200
    # Test with bad data
    response = client.post(
        f"/terminal/{terminal_id}/availability",
        headers={"Authorization": "Bearer " + user["token"]},
    )
    assert response.status_code == 422


@pytest.mark.usefixtures("get_logged_user")
def test_update_unavailability_period(get_logged_user):
    global terminal_id
    user = get_logged_user({"email": "jane@doe.com", "password": "janedoe"})
    # Test with good data
    updated_period = {"start_date": "2023-12-25", "end_date": "2023-12-27"}
    period_index = 0
    response = client.put(
        f"/terminal/{terminal_id}/availability/{period_index}",
        headers={"Authorization": "Bearer " + user["token"]},
        json=updated_period,
    )
    assert response.status_code == 200
    # Test with bad data
    response = client.put(
        f"/terminal/{terminal_id}/availability/{period_index}",
        headers={"Authorization": "Bearer " + user["token"]},
    )
    assert response.status_code == 422


@pytest.mark.usefixtures("get_logged_user")
def test_update_opening_hours(get_logged_user):
    global terminal_id
    user = get_logged_user({"email": "jane@doe.com", "password": "janedoe"})
    # Test with good data
    opening_hours = {
        "lundi": {"opening": "08:00", "closing": "18:00"},
        "mardi": {"opening": "08:00", "closing": "18:00"},
        "mercredi": {"opening": "08:00", "closing": "18:00"},
        "jeudi": {"opening": "08:00", "closing": "18:00"},
        "vendredi": {"opening": "08:00", "closing": "18:00"},
        "samedi": {"opening": "08:00", "closing": "18:00"},
        "dimanche": {"opening": "08:00", "closing": "18:00"},
    }
    response = client.put(
        f"/terminal/{terminal_id}/opening_hours",
        headers={"Authorization": "Bearer " + user["token"]},
        json=opening_hours,
    )
    assert response.status_code == 200
    # Test with bad data
    response = client.put(
        f"/terminal/{terminal_id}/opening_hours",
        headers={"Authorization": "Bearer " + user["token"]},
    )
    assert response.status_code == 422


@pytest.mark.usefixtures("get_logged_user")
def find_terminals_in_radius(get_logged_user):
    global terminal_id
    user = get_logged_user({"email": "jane@doe.com", "password": "janedoe"})
    # Test with good data
    latitude = 46
    longitude = 2
    radius = 50
    response = client.get(
        f"/terminals-in-radius/{latitude}/{longitude}/{radius}",
        headers={"Authorization": "Bearer " + user["token"]},
    )
    assert response.status_code == 200
    # Test with bad data
    latitude = 1000
    longitude = 1000
    radius = 0
    response = client.get(
        f"/terminals-in-radius/{latitude}/{longitude}/{radius}",
        headers={"Authorization": "Bearer " + user["token"]},
    )
    assert response.status_code == 422


@pytest.mark.usefixtures("get_logged_user")
def test_delete_terminal(get_logged_user):
    global terminal_id
    user = get_logged_user({"email": "jane@doe.com", "password": "janedoe"})
    # Test with existant id
    response = client.delete(
        f"/terminal/{terminal_id}", headers={"Authorization": "Bearer " + user["token"]}
    )
    assert response.status_code == 200
    # Test with inexistant id
    false_id = uuid.uuid4()
    response = client.delete(
        f"/terminal/{false_id}", headers={"Authorization": "Bearer " + user["token"]}
    )
    assert response.status_code == 404
    # Test with not creator id
    response = client.delete(f"/terminal/{terminal_id}")
    assert response.status_code == 401
