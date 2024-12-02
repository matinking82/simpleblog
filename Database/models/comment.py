from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import List, Optional
from sqlmodel import ForeignKey,Relationship
from datetime import date


class Comment(SQLModel, table=True):
    id: int = Field(primary_key=True)
    content: str
    created_at: date
    postId: int = Field(foreign_key="post.id")
    readerId: int = Field(foreign_key="user.id")