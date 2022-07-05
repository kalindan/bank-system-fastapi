# Bank system (https://github.com/kalindan/bank-system-fastpi/actions/workflows/python-app.yml/badge.svg)
The goal of this project is to create REST API service mimicing simple bank system and play with / learn FastAPI framework.
## User requirements:
- [X] Possibility to register customer
- [X] Possibility to create account(s) for given customer
- [X] Deposit/Withdraw money from account
- [X] Transfer money to another account
- [X] Set amount of allowed daily withdrawals
- [X] Set allowed maximum withdrawal per day
- [ ] Recover forgotten password by email
## Backend requirements:
- [X] Store persistent data in database
- [X] Authentication of customers by password flow
- [X] Endpoints secured by JWT
- [X] Validation of limits
- [X] Log all account transactions
- [X] Test suite
## Used technologies:
- Python
- FastAPI
- SQLModel
- Pytest
- PostgreSQL (Not implemented yet, locally running on SQLite)

## Bank system API endpoints
| Endpoints                          | HTTP method | Description                         |
|------------------------------------|-------------|-------------------------------------|
| /login                             |POST         | Login customer                      |
| /customers                         |POST         | Register new customer               |
| /customers/{customer_id}           |GET, DELETE  | Get / Delete customer               |
| /customers/{customer_id}/recover   |GET          | Recover password (Send to email)    |
| /accounts                          |POST         | Register new account                |
| /accounts/{account_id}             |GET, DELETE  | Get account info / Delete account   |
| /accounts/{account_id}/limits      |PUT          | Update account limits               |
| /accounts/{account_id}/transfer    |PUT          | Transfer money to different account |
| /accounts/{account_id}/withdrawal  |PUT          | Withdraw money from account         |
| /accounts/{account_id}/deposit     |PUT          | Deposit money to account            |
     

