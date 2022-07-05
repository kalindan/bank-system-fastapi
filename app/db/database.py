from sqlmodel import SQLModel, create_engine, Session
from decouple import config  # type:ignore

DB_URL = config("DB_URL")
connect_args = {"check_same_thread": False}
engine = create_engine(DB_URL, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
