from fastapi import APIRouter

from Database.services.userServices import UserServiceDep
from core.enums import UserRoles
from core.jwtHelper import JwtHelperDep, JwtPayload
from viewmodels.requests.admin.registerUserRequest import RegisterUserRequest
from viewmodels.requests.client.userLoginRequest import UserLoginRequest

router = APIRouter()


@router.post("/register")
async def register(user: RegisterUserRequest, userServices: UserServiceDep):
    new_user = await userServices.RegisterUser(user)

    if not new_user:
        return {"message": "User already exists", "success": False}

    return {"message": "User registered successfully", "success": True}


@router.post("/login")
async def login(
    user: UserLoginRequest, userServices: UserServiceDep, jwtHelper: JwtHelperDep
):
    loginuser = await userServices.loginUser(user)

    if not loginuser:
        return {"message": "Invalid credentials", "success": False}

    id = loginuser.id
    role = UserRoles.AUTHOR if loginuser.isAuthor else UserRoles.READER
    payload = JwtPayload(id=id, role=role)

    token = jwtHelper.createJWT(payload)

    return {"token": token, "success": True}
