import pytest
from app.models.account_model import Account
from app.db.database import get_session
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from fastapi.testclient import TestClient
from sqlmodel.pool import StaticPool


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def register_customer(name: str, email: str, password: str, client: TestClient):
    return client.post(
        url="/customers/",
        json={
            "name": name,
            "email": email,
            "password": password,
        },
    )


@pytest.fixture(name="jwt_token")
def get_jwt_token(client: TestClient):
    register_customer(
        name="Alfons",
        email="alfons@email.cz",
        password="1234567891",
        client=client,
    )
    yield client.post(
        url="/login",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": "alfons@email.cz", "password": "1234567891"},
    ).json()["access_token"]


def register_account(jwt_token: str, client: TestClient):
    return client.post(
        url="/accounts/",
        headers={"Authorization": f"Bearer {jwt_token}"},
        json={"daily_limit": "500", "num_of_withdrawals": "5"},
    )
