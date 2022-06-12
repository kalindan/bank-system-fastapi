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
- [ ] Store persistent data in database
- [ ] Authentication of customers
  [ ] 1. In first step by username and password
  [ ] 2. In second step by token
- [ ] Validation of limits
- [ ] Generate IDs for newly created customers and their accounts
- [ ] Bonus: Log all account transactions
## Used technologies:
- Python
- FastAPI
- SQLModel
- PostgreSQL

## Bank system API endpoints
|URL                                                                                         | HTTP method |
|---------------------------------------------                                               |-------------|
|http://127.0.0.1:8000/customer/registration                                                 |POST         |
|http://127.0.0.1:8000/customer/{customer_id}/info                                           |GET          |
|http://127.0.0.1:8000/customer/{customer_id}/termination                                    |DELETE       |
|http://127.0.0.1:8000/customer/{customer_id}/account/registration                           |POST         |
|http://127.0.0.1:8000/customer/{customer_id}/account/{account_id}/termination               |DELETE       |
|http://127.0.0.1:8000/customer/{customer_id}/account/{account_id}/limits                    |GET, POST    |
|http://127.0.0.1:8000/customer/{customer_id}/account/{account_id}/balance                   |GET          |
|http://127.0.0.1:8000/customer/{customer_id}/account/{account_id}/transfer                  |PUT          |
|http://127.0.0.1:8000/customer/{customer_id}/account/{account_id}/withdrawal                |PUT          |
|http://127.0.0.1:8000/customer/{customer_id}/account/{account_id}/deposit                   |PUT          |


