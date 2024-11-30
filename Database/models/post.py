from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import List, Optional
from sqlmodel import ForeignKey,Relationship


from .comment import Comment
from .tagPost import TagPost

class Post(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str
    content: str
    authorId: int = Field(default=None, foreign_key="user.id")