from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import List, Optional
from sqlmodel import ForeignKey, Relationship

from .tagPost import TagPost


class Tag(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(unique=True)
