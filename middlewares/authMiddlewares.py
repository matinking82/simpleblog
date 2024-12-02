from typing import Callable
from fastapi import FastAPI, HTTPException, Request, Response, Depends, status
from core.enums import UserRoles
from core.jwtHelper import JwtHelper
from starlette.middleware.base import BaseHTTPMiddleware

from routers import admin


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, jwtHelper: JwtHelper):
        super().__init__(app)
        self.jwtHelper = jwtHelper

    async def dispatch(self, req: Request, call_next: Callable):
        bearerToken = req.headers.get("Authorization")
        if not bearerToken:
            req.state.user = {"IsAuthenticated": False}
            return await call_next(req)

        parts = bearerToken.split(" ")
        if len(parts) != 2:
            req.state.user = {"IsAuthenticated": False}
            return await call_next(req)

        token = parts[1]

        if not token:
            req.state.user = {"IsAuthenticated": False}
            return await call_next(req)

        payload = self.jwtHelper.verifyJwt(token)

        if not payload:
            req.state.user = {"IsAuthenticated": False}
            return await call_next(req)

        req.state.user = {
            "IsAuthenticated": True,
            "Id": payload.id,
            "Role": payload.role,
        }
        return await call_next(req)


def protected_route(
    roles: list[UserRoles] = [UserRoles.ADMIN, UserRoles.READER, UserRoles.AUTHOR]
):
    def protect(request: Request):
        if (
            not request.state.user["IsAuthenticated"]
            or request.state.user["Role"] not in roles
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="not authorized"
            )
        return request.state.user

    return Depends(protect)
