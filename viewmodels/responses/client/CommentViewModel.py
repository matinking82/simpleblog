from pydantic import BaseModel
from datetime import date


class CommentViewModel(BaseModel):
    id: int
    readerId: int
    reader: str
    content: str
    created_at: date
    postId: int
