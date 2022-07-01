# Bank system
The goal of this project is to create REST API service mimicing simple bank system.
## User requirements:
- Possibility to register customer
- Possibility to create an account(s) for given customer
- Deposit/Withdraw money
- Transfer money to another account
- Set daily withdrawal limits
- Set maximum per withdrawal limit
## Backend requirements:
- [ ] Store persistent data in database
- [ ] Authentication of customers
  1. [ ] In first step by username and password
  2. [ ] In second step by token
- [ ] Validation of limits
- [ ] Generate IDs for newly created customers and their accounts
- [ ] Bonus: Log all account transactions
## Used technologies:
- Python
- FastAPI
- SQLModel
- PostgreSQL

## Bank system API endpoints
| Endpoints                          | HTTP method      | Description                                |
|------------------------------------|------------------|--------------------------------------------|
| /customers                         |POST, GET, DELETE | Register Get / Delete customer             |
| /customers/{customer_id}/recover   |GET               | Recover password (Send to email)           |
| /accounts                          |POST              | Register new account                       |
| /accounts/{account_id}             |GET, DELETE       | Get account info / Delete account          |
| /accounts/{account_id}/limits      |POST              | Set account daily / max amount limits      |
| /accounts/{account_id}/transfer    |PUT               | Transfer money to different account        |
| /accounts/{account_id}/withdrawal  |PUT               | Withdraw money from account                |
| /accounts/{account_id}/deposit     |PUT               | Deposit money to account                   |
     

