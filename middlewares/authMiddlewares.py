from typing import Callable
from fastapi import HTTPException, Request, Depends, status
from Database.services.userServices import UserServiceDep
from core.enums import UserRoles
from core.jwtHelper import JwtHelperDep


def protected_route(
    roles: list[UserRoles] = [UserRoles.ADMIN, UserRoles.READER, UserRoles.AUTHOR],
):
    async def protect(
        request: Request,
        jwtHelper: JwtHelperDep,
        userServices: UserServiceDep,
    ):
        bearerToken = request.headers.get("Authorization")
        if not bearerToken:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )

        parts = bearerToken.split(" ")
        if len(parts) != 2:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )

        token = parts[1]

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )

        payload = jwtHelper.verifyJwt(token)

        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
            )

        role = payload.role

        if role != UserRoles.ADMIN:
            result = await userServices.validateUser(id=payload.id)
            if not result["success"]:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
                )
            role = UserRoles.AUTHOR if result["user"].isAuthor else UserRoles.READER

        if role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )

        return {
            "Id": payload.id,
            "Role": role,
        }

    return Depends(protect)
