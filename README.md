# Bank system
The goal of this project is to create simple REST API service mimicing simple bank system.
## User requirements:
- Possibility to register customer
- Possibility to create an account(s) for given customer
- Deposit/Withdraw money
- Transfer money to another account
- Set daily withdrawal limits
- Set maximum per withdrawal limit
## Backend requirements:
- Store persistent data in database
- Authentication of customers
- Validation of limits
- Generate 10 digit account number
## Used technologies:
- Python
- FastAPI
- SQLModel
- PostgreSQL

## Bank system API endpoints
|URL                                      | HTTP method |
|-----------------------------------------|-------------|
|http://127.0.0.1:8000/register-customer  |POST         |
|http://127.0.0.1:8000/create-account     |POST         |
|http://127.0.0.1:8000/set-limits         |POST         |
|http://127.0.0.1:8000/get-balance        |GET          |
|http://127.0.0.1:8000/get-limits         |GET          |
|http://127.0.0.1:8000/transfer-money     |PUT          |
|http://127.0.0.1:8000/withdraw-money     |PUT          |
|http://127.0.0.1:8000/deposit-money      |PUT          |
|http://127.0.0.1:8000/delete-account     |DELETE       |
|http://127.0.0.1:8000/delete-customer    |DELETE       |
