import pytest
from app.models import Account
from app.models.transaction_model import Transaction
from app.tests.conftest import register_account
from app.utils.enums import TransactionType
from fastapi import Depends, HTTPException
from fastapi.testclient import TestClient
from sqlmodel import Session


def test_check_balance_exception(
    jwt_token: str, client: TestClient, session: Session
):
    register_account(jwt_token=jwt_token, client=client)
    with pytest.raises(HTTPException):
        account = Account(id=1).db_read(session=session).check_balance(600.0)


def test_check_daily_withdrawals_exception(
    jwt_token: str, client: TestClient, session: Session
):
    register_account(jwt_token=jwt_token, client=client)
    [
        Transaction(
            account_id=1,
            transaction_type=TransactionType.WITHDRAWAL,
            amount=10,
        ).db_create(session=session)
        for _ in range(11)
    ]
    with pytest.raises(HTTPException):
        Account(id=1).db_read(session=session).check_daily_withdrawals()


def test_check_amount_withdrawn_exception(
    jwt_token: str, client: TestClient, session: Session
):
    register_account(jwt_token=jwt_token, client=client)
    Transaction(
        account_id=1,
        transaction_type=TransactionType.WITHDRAWAL,
        amount=190,
    ).db_create(session=session)
    with pytest.raises(HTTPException):
        Account(id=3).db_read(session=session).check_amount_withdrawn(20)
