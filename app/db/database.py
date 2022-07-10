from sqlmodel import SQLModel, create_engine, Session
from app.config.config import active_config


engine = create_engine(active_config.db_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
