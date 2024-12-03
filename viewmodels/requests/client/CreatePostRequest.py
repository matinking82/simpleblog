from pydantic import BaseModel


class CreatePostRequest(BaseModel):
    title: str
    content: str
    tags: list[str]
