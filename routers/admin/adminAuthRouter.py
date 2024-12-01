from fastapi import APIRouter

from Database.services.adminServices import AdminServiceDep
from core.enums import UserRoles
from core.jwtHelper import JwtHelperDep, JwtPayload
from viewmodels.requests.admin.adminLoginRequest import AdminLoginRequest
from viewmodels.requests.admin.registerAdminRequest import RegisterAdminRequest

router = APIRouter()


@router.post("/register")
async def register(admin: RegisterAdminRequest, adminServices: AdminServiceDep):
    new_admin = adminServices.registerAdmin(admin)

    if not new_admin:
        return {
            "message": "Something went wrong when trying to register",
            "success": False,
        }

    return {"message": "Admin registered successfully", "success": True}


@router.post("/login")
async def login(
    admin: AdminLoginRequest, adminServices: AdminServiceDep, jwtHelper: JwtHelperDep
):
    loginAdmin = adminServices.loginAdmin(admin)

    if not loginAdmin:
        return {"message": "Invalid credentials", "success": False}

    id = loginAdmin.id
    role = UserRoles.ADMIN
    payload = JwtPayload(id=id, role=role)

    token = jwtHelper.createJWT(payload)

    return {"token": token, "success": True}
