from Database.services.repositories.userRepository import UserRepositoryDep
from Database.models.user import User
from sqlmodel import select
from typing import Annotated
from fastapi import Depends


class userServices:
    def __init__(self, userRepository: UserRepositoryDep):
        self.adminRepository = userRepository


UserServiceDep = Annotated[userServices, Depends(userServices)]
