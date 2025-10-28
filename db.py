from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated, Any, Generator


db_name = "tienda.sqlite3"
db_url = f"sqlite:///{db_name}"

engine = create_engine(db_url)

def create_tables(app:FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]