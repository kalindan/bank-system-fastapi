import uvicorn  # type:ignore
from fastapi import FastAPI
from app.db import create_db_and_tables
from app.routers import accounts, customers, login

app = FastAPI(title="Bank system")
app.include_router(login.router)
app.include_router(customers.router)
app.include_router(accounts.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def index():
    return {"message": "Welcome to bank system"}
