from fastapi.testclient import TestClient
from tests.conftest import register_account


def test_register_account(jwt_token: str, client: TestClient):
    response = register_account(jwt_token=jwt_token, client=client)
    data = response.json()
    assert response.status_code == 201
    assert data["daily_limit"] == 500
    assert data["num_of_withdrawals"] == 5
    assert data["message"] == "Account successfully registered"


def test_register_account_no_login(client: TestClient):
    response = client.post(
        url="/accounts/",
        json={"daily_limit": "500", "num_of_withdrawals": "5"},
    )
    assert response.status_code == 401


def test_get_account(jwt_token: str, client: TestClient):
    register_account(jwt_token=jwt_token, client=client)
    response = client.get(
        url="/accounts/1", headers={"Authorization": f"Bearer {jwt_token}"}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["daily_limit"] == 500
    assert data["num_of_withdrawals"] == 5
    assert data["message"] == "Account successfully loaded"


def test_get_account_invalid_id(jwt_token: str, client: TestClient):
    register_account(jwt_token=jwt_token, client=client)
    response = client.get(
        url="/accounts/2", headers={"Authorization": f"Bearer {jwt_token}"}
    )
    data = response.json()
    assert response.status_code == 404


def test_get_account_no_login(jwt_token: str, client: TestClient):
    register_account(jwt_token=jwt_token, client=client)
    response = client.get(url="/accounts/1")
    data = response.json()
    assert response.status_code == 401


def test_update_limits(jwt_token: str, client: TestClient):
    register_account(jwt_token=jwt_token, client=client)
    response = client.patch(
        url="/accounts/1/limits",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"daily_limit": "750", "num_of_withdrawals": "45"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["daily_limit"] == 750
    assert data["num_of_withdrawals"] == 45
    assert data["message"] == "Account 1 limits successfully updated"


def test_update_limits_invalid_value(jwt_token: str, client: TestClient):
    register_account(jwt_token=jwt_token, client=client)
    response = client.patch(
        url="/accounts/1/limits",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"daily_limit": "-750", "num_of_withdrawals": "45"},
    )
    data = response.json()
    assert response.status_code == 422


def test_delete_account(jwt_token: str, client: TestClient):
    register_account(jwt_token=jwt_token, client=client)
    response = client.delete(
        url="/accounts/1",
        headers={"Authorization": f"Bearer {jwt_token}"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Account 1 successfully deleted"
    response_2 = client.get(
        url="/accounts/1", headers={"Authorization": f"Bearer {jwt_token}"}
    )
    assert response_2.status_code == 404


def test_deposit_money(jwt_token: str, client: TestClient):
    register_account(jwt_token=jwt_token, client=client)
    response = client.patch(
        url="/accounts/1/deposit",
        headers={"Authorization": f"Bearer {jwt_token}"},
        data="1022",
    )
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Successfully deposited 1022.0 CZK to account 1"


def test_deposit_invalid_amount(jwt_token: str, client: TestClient):
    register_account(jwt_token=jwt_token, client=client)
    response = client.patch(
        url="/accounts/1/deposit",
        headers={"Authorization": f"Bearer {jwt_token}"},
        data="-10",
    )
    data = response.json()
    assert response.status_code == 422


def test_withdraw_money(jwt_token: str, client: TestClient):
    register_account(jwt_token=jwt_token, client=client)
    client.patch(
        url="/accounts/1/deposit",
        headers={"Authorization": f"Bearer {jwt_token}"},
        data="1000",
    )
    response = client.patch(
        url="/accounts/1/withdrawal",
        headers={"Authorization": f"Bearer {jwt_token}"},
        data="250",
    )
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Successfully withdrawn 250.0 CZK from account 1"


def test_transfer_money(jwt_token: str, client: TestClient):
    register_account(jwt_token=jwt_token, client=client)
    register_account(jwt_token=jwt_token, client=client)
    client.patch(
        url="/accounts/1/deposit",
        headers={"Authorization": f"Bearer {jwt_token}"},
        data="1000",
    )
    response = client.patch(
        url="/accounts/1/transfer",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"to_account_id": "2", "amount": "250"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["message"] == "Successfully  transferred 250.0 CZK to account 2"
