from core.passwordHasher import PasswordHasherDep
from viewmodels.requests.admin.registerUserRequest import RegisterUserRequest
from Database.services.repositories.userRepository import UserRepositoryDep
from Database.models.user import User

from sqlmodel import select
from typing import Annotated
from fastapi import Depends
from datetime import datetime

from viewmodels.requests.client.userLoginRequest import UserLoginRequest


class UserServices:
    def __init__(
        self, userRepository: UserRepositoryDep, passwordHasher: PasswordHasherDep
    ):
        self.adminRepository = userRepository
        self.passwordHasher = passwordHasher

    async def RegisterUser(self, request: RegisterUserRequest):
        # Hash the password
        hashed_password = self.passwordHasher.HashPassword(request.password)
        # Create a new user
        new_user = User(
            username=request.username,
            passwordHash=hashed_password,
            created_at=datetime.now(),
            isAuthor=request.isAuthor,
        )
        # Add the user to the database
        success = self.adminRepository.Create(new_user)

        if success:
            return new_user

        return None

    async def loginUser(self, request: UserLoginRequest):
        user = self.adminRepository.GetByUsername(request.username)
        if not user:
            return None

        if self.passwordHasher.VerifyPassword(request.password, user.passwordHash):
            return user

        return None

    async def validateUser(self, id: int):
        return self.adminRepository.GetById(id)


UserServiceDep = Annotated[UserServices, Depends(UserServices)]
