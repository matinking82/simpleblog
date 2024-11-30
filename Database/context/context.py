from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated
from fastapi import Depends
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
