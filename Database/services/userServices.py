from core.enums import UserRoles
from core.jwtHelper import JwtHelperDep, JwtPayload
from core.passwordHasher import PasswordHasherDep
from viewmodels.requests.admin.changeUserRoleRequest import ChangeUserRoleRequest
from viewmodels.requests.admin.registerUserRequest import RegisterUserRequest
from Database.services.repositories.userRepository import UserRepositoryDep
from Database.models.user import User

from sqlmodel import select
from typing import Annotated
from fastapi import Depends
from datetime import datetime

from viewmodels.requests.client.userLoginRequest import UserLoginRequest
from viewmodels.responses.client.UserViewModel import UserViewModel


class UserServices:
    def __init__(
        self,
        userRepository: UserRepositoryDep,
        passwordHasher: PasswordHasherDep,
        jwtHelper: JwtHelperDep,
    ):
        self.userRepository = userRepository
        self.passwordHasher = passwordHasher
        self.jwtHelper = jwtHelper

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
        success = self.userRepository.Create(new_user)

        if success:
            return {
                "message": "User registered successfully",
                "success": True,
                "user": UserViewModel(
                    id=new_user.id,
                    username=new_user.username,
                    isAuthor=new_user.isAuthor,
                    created_at=new_user.created_at,
                ),
            }

        return {
            "message": "User already exists",
            "success": False,
        }

    async def loginUser(self, request: UserLoginRequest):
        user = self.userRepository.GetByUsername(request.username)
        if not user:
            raise {
                "message": "User not found",
                "success": False,
            }

        if self.passwordHasher.VerifyPassword(request.password, user.passwordHash):
            token = self.jwtHelper.createJWT(
                JwtPayload(
                    id=user.id,
                    role=UserRoles.AUTHOR if user.isAuthor else UserRoles.READER,
                )
            )
            return {
                "success": True,
                "message": "User logged in successfully",
                "token": token,
                "token_type": "bearer",
            }

        return {
            "message": "Invalid credentials",
            "success": False,
        }

    async def validateUser(self, id: int):
        user = self.userRepository.GetById(id)

        if not user:
            return {
                "message": "User not found",
                "success": False,
            }

        return {
            "message": "User found",
            "success": True,
            "user": UserViewModel(
                id=user.id,
                username=user.username,
                isAuthor=user.isAuthor,
                created_at=user.created_at,
            ),
        }

    async def setRole(self, request: ChangeUserRoleRequest):
        user = self.userRepository.GetByUsername(request.username)

        if not user:
            return {
                "message": "User not found",
                "success": False,
            }

        user.isAuthor = request.isAuthor

        success = self.userRepository.Update(user)

        if success:
            return {
                "message": "Role updated successfully",
                "success": True,
            }

        return {
            "message": "Failed to update role",
            "success": False,
        }

    async def GetAllUsers(self, page: int, pageSize: int):
        users = self.userRepository.GetAll(page, pageSize)

        return {
            "message": "Users found",
            "success": True,
            "users": [
                UserViewModel(
                    id=user.id,
                    username=user.username,
                    isAuthor=user.isAuthor,
                    created_at=user.created_at,
                )
                for user in users
            ],
        }


UserServiceDep = Annotated[UserServices, Depends(UserServices)]
