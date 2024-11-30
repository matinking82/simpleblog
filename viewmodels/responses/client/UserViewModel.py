from pydantic import BaseModel
from datetime import date


class UserViewModel(BaseModel):
    id: int
    username: str
    isAuthor: bool
    created_at: date
