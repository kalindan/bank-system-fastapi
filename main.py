from fastapi import FastAPI, Query
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class Account(BaseModel):
    email:str
    password:str = Query(min_length=10)

@app.get("/")
def index():
    return "Hello World"

@app.post("/create-account")
def create_account(new_account: NewAccount):
    return f"Your email is {new_account.email} and your password is {new_account.password}"

if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)
