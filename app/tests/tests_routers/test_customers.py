import pytest
from requests import Response  # type:ignore
from fastapi.testclient import TestClient
from app.tests.conftest import register_customer


def test_register_customer(client: TestClient):
    response = register_customer(
        name="Alfons",
        email="alfons@email.cz",
        password="1234567891",
        client=client,
    )
    data = response.json()
    assert response.status_code == 201
    assert data["name"] == "Alfons"
    assert data["email"] == "alfons@email.cz"


def test_register_existing_customer(client: TestClient):
    register_customer(
        name="Alfons",
        email="alfons@email.cz",
        password="1234567891",
        client=client,
    )
    response = register_customer(
        name="Alfons",
        email="alfons@email.cz",
        password="1234567891",
        client=client,
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Email already registered"


def test_register_customer_invalid(client: TestClient):
    response = client.post(
        url="/customers/",
        json={
            "wrong_tag": 123,
            "email": "alfons@email.cz",
            "password": "12345678910",
        },
    )
    assert response.status_code == 422


def test_register_customer_incomplete(client: TestClient):
    response = client.post(
        url="/customers/",
        json={
            "email": "alfons@email.cz",
            "password": "12345678910",
        },
    )
    assert response.status_code == 422


def test_get_customer_info(jwt_token: str, client: TestClient):
    get_customer = client.get(
        url="/customers/1",
        headers={"Authorization": f"Bearer {jwt_token}"},
    )
    data = get_customer.json()
    assert get_customer.status_code == 200
    assert data["id"] == 1


def test_get_customer_info_wrong_id(jwt_token: str, client: TestClient):
    get_customer = client.get(
        url="/customers/2",
        headers={"Authorization": f"Bearer {jwt_token}"},
    )
    data = get_customer.json()
    assert get_customer.status_code == 401
    assert data["detail"] == "Not authorized to view this customer profile"


def test_get_customer_info_no_login(client: TestClient):
    get_customer = client.get(
        url="/customers/2",
    )
    data = get_customer.json()
    assert get_customer.status_code == 401
    assert data["detail"] == "Not authenticated"


def test_delete_customer(jwt_token: str, client: TestClient):
    delete_customer = client.delete(
        url="/customers/1",
        headers={"Authorization": f"Bearer {jwt_token}"},
    )
    data = delete_customer.json()
    assert delete_customer.status_code == 200
    assert data["message"] == "Customer 1 successfully deleted"
    get_customer = client.get(
        url="/customers/1",
        headers={"Authorization": f"Bearer {jwt_token}"},
    )
    assert get_customer.status_code == 404
