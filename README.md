# Bank system
The goal of this project is to create REST API service mimicing simple bank system and play with / learn FastAPI framework.
## User requirements:
- [X] Possibility to register customer
- [X] Possibility to create an account(s) for given customer
- [X] Deposit/Withdraw money
- [ ] Transfer money to another account
- [X] Set daily withdrawal limits
- [X] Set maximum per withdrawal limit
## Backend requirements:
- [X] Store persistent data in database
- [X] Authentication of customers by password flow and JWT
- [X] Validation of limits
- [X] Log all account transactions
## Used technologies:
- Python
- FastAPI
- SQLModel
- PostgreSQL (Locally running on SQLite)

## Bank system API endpoints
| Endpoints                          | HTTP method      | Description                                |
|------------------------------------|------------------|--------------------------------------------|
| /login                             |POST              | Login customer                             |
| /customers                         |POST, GET, DELETE | Register / Get / Delete customer           |
| /customers/{customer_id}/recover   |GET               | Recover password (Send to email)           |
| /accounts                          |POST              | Register new account                       |
| /accounts/{account_id}             |GET, DELETE       | Get account info / Delete account          |
| /accounts/{account_id}/limits      |POST              | Set account daily / max amount limits      |
| /accounts/{account_id}/transfer    |PUT               | Transfer money to different account        |
| /accounts/{account_id}/withdrawal  |PUT               | Withdraw money from account                |
| /accounts/{account_id}/deposit     |PUT               | Deposit money to account                   |
     

