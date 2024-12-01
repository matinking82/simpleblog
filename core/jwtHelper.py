import os
import datetime
from enum import Enum
from fastapi import Depends
from typing import Annotated
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta, timezone

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
        self.ALGORITHM = "HS512"

    def createJWT(self, payload: JwtPayload, expday=30):
        expire = datetime.now(timezone.utc) + timedelta(expday * 24 * 60)
        to_encode = {
            "id": payload.id,
            "role": payload.role.value,
        }
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def verifyJwt(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return JwtPayload(id=payload["id"], role=UserRoles(payload["role"]))
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


JwtHelperDep = Annotated[JwtHelper, Depends(JwtHelper)]
