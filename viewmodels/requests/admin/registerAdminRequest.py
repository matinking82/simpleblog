from pydantic import BaseModel

class RegisterAdminRequest(BaseModel):
    username: str
    password: str
