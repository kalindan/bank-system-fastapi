import uvicorn  # type:ignore
from fastapi import FastAPI
from app.db import create_db_and_tables
from app.routers import accounts, customers, login

app = FastAPI()
app.include_router(login.router)
app.include_router(customers.router)
app.include_router(accounts.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def index():
    return {"message": "Welcome to k-bank system"}


# if __name__ == "__main__":
#     uvicorn.run("main:app",reload=True)
