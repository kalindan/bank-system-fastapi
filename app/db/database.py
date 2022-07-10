from sqlmodel import SQLModel, create_engine, Session
from app.config.config import config

connect_args = {"check_same_thread": False}
engine = create_engine(config().db_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
