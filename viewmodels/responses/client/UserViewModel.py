from pydantic import BaseModel
from datetime import datetime


class UserViewModel(BaseModel):
    id: int
    username: str
    isAuthor: bool
    created_at: datetime
