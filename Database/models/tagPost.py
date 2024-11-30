from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import List, Optional
from sqlmodel import ForeignKey,Relationship

class TagPost(SQLModel, table=True):
    tagId: int = Field(primary_key=True, foreign_key="tag.id")
    postId: int = Field(primary_key=True, foreign_key="post.id")