from Database.services.repositories.adminRepository import AdminRepositoryDep
from Database.models.admin import Admin
from sqlmodel import select
from typing import Annotated
from fastapi import Depends
from datetime import datetime

from core.passwordHasher import PasswordHasherDep
from viewmodels.requests.admin.adminLoginRequest import AdminLoginRequest
from viewmodels.requests.admin.registerAdminRequest import RegisterAdminRequest


class AdminServices:
    def __init__(
        self, adminRepository: AdminRepositoryDep, passwordHasher: PasswordHasherDep
    ):
        self.adminRepository = adminRepository
        self.passwordHasher = passwordHasher

    def registerAdmin(self, request: RegisterAdminRequest):
        admin = Admin(
            username=request.username,
            password=self.passwordHasher.HashPassword(request.password),
            created_at=datetime.now(),
        )

        success = self.adminRepository.Create(admin)

        if success:
            return admin

        return None

    def loginAdmin(self, request: AdminLoginRequest):
        admin = self.adminRepository.GetByUsername(request.username)
        if not admin:
            return None

        if self.passwordHasher.VerifyPassword(request.password, admin.password):
            return admin

        return None

    def validateAdmin(self, id: int):
        return self.adminRepository.GetById(id)


AdminServiceDep = Annotated[AdminServices, Depends(AdminServices)]
