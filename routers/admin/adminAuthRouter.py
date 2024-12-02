from fastapi import APIRouter, HTTPException, status, Request, Depends

from Database.services.adminServices import AdminServiceDep
from core.enums import UserRoles
from core.jwtHelper import JwtHelperDep, JwtPayload
from middlewares.authMiddlewares import protected_route
from viewmodels.requests.admin.adminLoginRequest import AdminLoginRequest
from viewmodels.requests.admin.registerAdminRequest import RegisterAdminRequest

router = APIRouter()


@router.post("/register")
async def register(
    admin: RegisterAdminRequest,
    adminServices: AdminServiceDep,
    authUser: dict = protected_route([UserRoles.ADMIN]),
):
    result = adminServices.registerAdmin(admin)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"]
        )

    return result


@router.post("/login")
async def login(admin: AdminLoginRequest, adminServices: AdminServiceDep):
    result = adminServices.loginAdmin(admin)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"]
        )

    return result


@router.get("/validate")
async def validate(
    adminServices: AdminServiceDep,
    authUser: dict = protected_route([UserRoles.ADMIN]),
):
    result = await adminServices.validateAdmin(authUser["Id"])

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="not authorized"
        )

    return result
