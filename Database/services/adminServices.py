from Database.services.repositories.adminRepository import AdminRepositoryDep
from Database.models.admin import Admin
from sqlmodel import select
from typing import Annotated
from fastapi import Depends



class AdminServices:
    def __init__(self, adminRepository: AdminRepositoryDep):
        self.adminRepository = adminRepository


AdminServiceDep = Annotated[AdminServices, Depends(AdminServices)]