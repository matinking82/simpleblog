from pydantic import BaseModel
from datetime import date


class PostsFilter(BaseModel):
    keyword: str | None
    tags: list[str] | None
    author: str | None
    startDate: date | None
    endDate: date | None
