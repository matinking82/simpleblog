from fastapi import APIRouter, HTTPException, status, Request

from Database.services.adminServices import AdminServiceDep
from core.enums import UserRoles
from core.jwtHelper import JwtHelperDep, JwtPayload
from viewmodels.requests.admin.adminLoginRequest import AdminLoginRequest
from viewmodels.requests.admin.registerAdminRequest import RegisterAdminRequest

router = APIRouter()


@router.post("/register")
async def register(admin: RegisterAdminRequest, adminServices: AdminServiceDep):
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
async def validate(request: Request, adminServices: AdminServiceDep):
    if (
        not request.state.user["IsAuthenticated"]
        or request.state.user["Role"] != UserRoles.ADMIN
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="not authorized"
        )

    result = await adminServices.validateAdmin(request.state.user["Id"])

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="not authorized"
        )

    return result
