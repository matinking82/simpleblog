from pydantic import BaseModel
from datetime import date


class PostViewModel(BaseModel):
    id: int
    title: str
    content: str
    authorId: int | None
    author: str | None
    tags: list[str]
    created_at: date
    updated_at: date
