from pydantic import BaseModel


class UpdaetPostRequest(BaseModel):
    title: str | None
    content: str | None
