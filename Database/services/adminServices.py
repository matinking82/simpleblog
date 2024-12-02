from Database.services.repositories.adminRepository import AdminRepositoryDep
from Database.models.admin import Admin
from sqlmodel import select
from typing import Annotated
from fastapi import Depends
from datetime import datetime

from core.enums import UserRoles
from core.jwtHelper import JwtHelperDep, JwtPayload
from core.passwordHasher import PasswordHasherDep
from viewmodels.requests.admin.adminLoginRequest import AdminLoginRequest
from viewmodels.requests.admin.registerAdminRequest import RegisterAdminRequest
from viewmodels.responses.admin.AdminViewModel import AdminViewModel


class AdminServices:
    def __init__(
        self,
        adminRepository: AdminRepositoryDep,
        passwordHasher: PasswordHasherDep,
        jwtHelper: JwtHelperDep,
    ):
        self.adminRepository = adminRepository
        self.passwordHasher = passwordHasher
        self.jwtHelper = jwtHelper

    def registerAdmin(self, request: RegisterAdminRequest):
        admin = Admin(
            username=request.username,
            password=self.passwordHasher.HashPassword(request.password),
            created_at=datetime.now(),
        )

        success = self.adminRepository.Create(admin)

        if success:
            return {
                "message": "Admin registered successfully",
                "success": True,
                "admin": AdminViewModel(
                    id=admin.id, username=admin.username, created_at=admin.created_at
                ),
            }

        return {
            "message": "Admin already exists",
            "success": False,
        }

    def loginAdmin(self, request: AdminLoginRequest):
        admin = self.adminRepository.GetByUsername(request.username)
        if not admin:
            return {
                "message": "Admin not found",
                "success": False,
            }

        if self.passwordHasher.VerifyPassword(request.password, admin.password):
            token = self.jwtHelper.createJWT(
                JwtPayload(id=admin.id, role=UserRoles.ADMIN)
            )

            return {
                "message": "Admin logged in successfully",
                "success": True,
                "token": token,
                "token_type": "bearer",
            }

        return {
            "message": "Invalid password",
            "success": False,
        }

    async def validateAdmin(self, id: int):
        admin = self.adminRepository.GetById(id)

        if not admin:
            return {
                "message": "Admin not found",
                "success": False,
            }

        return {
            "message": "Admin validated",
            "success": True,
            "admin": AdminViewModel(
                id=admin.id, username=admin.username, created_at=admin.created_at
            ),
        }


AdminServiceDep = Annotated[AdminServices, Depends(AdminServices)]
