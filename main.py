import uvicorn  #type:ignore
from application import app

if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)
