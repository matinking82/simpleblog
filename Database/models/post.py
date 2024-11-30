from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import List, Optional
from sqlmodel import ForeignKey, Relationship
from datetime import date


class Post(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str
    content: str
    authorId: int = Field(default=None, foreign_key="user.id")
    created_at: date
    updated_at: date
