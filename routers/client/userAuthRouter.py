from fastapi import APIRouter, HTTPException, Request, status

from Database.services.userServices import UserServiceDep
from core.enums import UserRoles
from viewmodels.requests.admin.registerUserRequest import RegisterUserRequest
from viewmodels.requests.client.userLoginRequest import UserLoginRequest

router = APIRouter()


@router.post("/register")
async def register(
    request: Request, user: RegisterUserRequest, userServices: UserServiceDep
):
    if (
        not request.state.user["IsAuthenticated"]
        or request.state.user["Role"] != UserRoles.ADMIN
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="not authorized"
        )

    result = await userServices.RegisterUser(user)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"]
        )

    return result


@router.post("/login")
async def login(user: UserLoginRequest, userServices: UserServiceDep):
    result = await userServices.loginUser(user)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"]
        )

    return result


@router.get("/validate")
async def validate(request: Request, userServices: UserServiceDep):
    if not request.state.user["IsAuthenticated"]:
        return {
            "message": "Token is invalid",
            "success": False,
        }
    print(request.state.user)
    result = await userServices.validateUser(request.state.user["Id"])

    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="not authorized"
        )

    return result
