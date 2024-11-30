from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import List, Optional
from sqlmodel import ForeignKey, Relationship

from .comment import Comment
from .post import Post


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str = Field(unique=True)
    passwordHash: str
    isAuthor: bool
