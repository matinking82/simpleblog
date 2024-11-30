from pydantic import BaseModel


class AdminViewModel(BaseModel):
    id: int
    username: str
    created_at: str