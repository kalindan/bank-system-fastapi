# Bank system
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
- [ ] New customer verification by email
- [X] Authentication of customers by password flow
- [X] Endpoints secured by JWT
  - [X] Generate access token
  - [ ] Generate refresh token
  - [ ] Black listing access token
- [X] Validation of limits
- [X] Log all account transactions
- [X] Test suite ![example workflow](https://github.com/kalindan/bank-system-fastapi/actions/workflows/python-app.yml/badge.svg)
- [X] Run on Docker
- [ ] Logging 
- [ ] Caching transactions read from db
## Used technologies:
- Python
- FastAPI
- SQLModel
- Pytest
- PostgreSQL (for test suite SQLite used)

## Bank system API endpoints
| Endpoints                          | HTTP method | Description                         |
|------------------------------------|-------------|-------------------------------------|
| /login                             |POST         | Login customer                      |
| /customers                         |POST         | Register new customer               |
| /customers/{customer_id}           |GET, DELETE  | Get / Delete customer               |
| /customers/{customer_id}/recover   |GET          | Recover password (Send to email)    |
| /accounts                          |POST         | Register new account                |
| /accounts/{account_id}             |GET, DELETE  | Get account info / Delete account   |
| /accounts/{account_id}/limits      |PATCH        | Update account limits               |
| /accounts/{account_id}/transfer    |PATCH        | Transfer money to different account |
| /accounts/{account_id}/withdrawal  |PATCH        | Withdraw money from account         |
| /accounts/{account_id}/deposit     |PATCH        | Deposit money to account            |

