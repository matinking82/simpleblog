from pydantic import BaseModel


class ChangeUserRoleRequest(BaseModel):
    username: str
    isAuthor: bool
