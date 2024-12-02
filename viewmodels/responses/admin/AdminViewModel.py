from pydantic import BaseModel
from datetime import datetime

class AdminViewModel(BaseModel):
    id: int
    username: str
    created_at: datetime