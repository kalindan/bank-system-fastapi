import pytest

from app.models.account_model import Account
from ..db.database import connect_args
from sqlmodel import SQLModel, Session, create_engine

sqlite_file_name = "test_db.db"
sqlite_url = f"sqlite:///tests/{sqlite_file_name}"
engine = create_engine(sqlite_url, connect_args=connect_args)


@pytest.fixture(autouse=True)
def create_test_db():
    SQLModel.metadata.create_all(engine)
    [
        Account(
            id=id, balance=500, daily_limit=200, num_of_withdrawals=10
        ).db_create(session=get_test_session())
        for id in range(2, 10)
    ]
    yield
    SQLModel.metadata.drop_all(engine)


def get_test_session():
    with Session(engine) as session:
        return session
