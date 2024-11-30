from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from datetime import date

class Admin(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(unique=True)
    password: str
    created_at: date