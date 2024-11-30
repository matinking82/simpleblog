import os
from jose import jwt, JWTError
import datetime
from enum import Enum
from fastapi import Depends
from typing import Annotated
from pydantic import BaseModel

from core.enums import UserRoles


class JwtPayload:
    id: int
    role: UserRoles

    def __init__(self, id: int = None, role: UserRoles = None):
        self.id = id
        self.role = role

class JwtHelper:
    def __init__(self):
        self.SECRET_KEY = os.getenv("JWT_SECRET")
        self.ALGORITHM = "HS256"

    def createJWT(self, payload: JwtPayload, expday=30):
        payload.exp = datetime.datetime.utcnow() + datetime.timedelta(days=expday)
        encoded_jwt = jwt.encode(
            {
                "id": payload.id,
                "role": payload.role.value,
            }, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_jwt

    def verifyJwt(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

            result = JwtPayload()
            result.id = payload["id"]
            result.role = UserRoles(payload["role"])

            if (
                datetime.datetime.utcfromtimestamp(payload["exp"])
                < datetime.datetime.utcnow()
            ):
                raise JWTError

            return result
        except JWTError:
            return None


JwtHelperDep = Annotated[JwtHelper, Depends(JwtHelper)]
