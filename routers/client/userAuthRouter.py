from fastapi import APIRouter, HTTPException, Request, status, Depends

from Database.services.userServices import UserServiceDep
from core.enums import UserRoles
from middlewares.authMiddlewares import protected_route
from viewmodels.requests.admin.registerUserRequest import RegisterUserRequest
from viewmodels.requests.client.userLoginRequest import UserLoginRequest

router = APIRouter()


@router.post("/register")
async def register(
    userRequest: RegisterUserRequest,
    userServices: UserServiceDep,
    authUser: dict = Depends(protected_route([UserRoles.ADMIN])),
):
    print(authUser)
    result = await userServices.RegisterUser(userRequest)

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
async def validate(
    userServices: UserServiceDep,
    authUser: dict = Depends(protected_route([UserRoles.READER, UserRoles.AUTHOR])),
):
    result = await userServices.validateUser(authUser["Id"])

    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="not authorized"
        )

    return result
