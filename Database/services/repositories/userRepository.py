from fastapi import Depends
from typing import Annotated
from sqlmodel import select

from Database.context.context import SessionDep
from Database.models.user import User


class UserRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def Create(self, user: User) -> bool:
        self.session.add(user)
        self.session.commit()
        return True

    def GetById(self, user_id) -> User:
        return self.session.exec(select(User).where(User.id == user_id)).first()

    def GetByUsername(self, username) -> User:
        return self.session.exec(select(User).where(User.username == username)).first()

    def GetAll(self, page=1, pageSize=100, filter=None) -> list[User]:
        return self.session.exec(
            select(User).limit(pageSize).offset((page - 1) * pageSize).filter(filter)
        ).all()

    def Update(self, user: User) -> bool:
        self.session.merge(user)
        self.session.commit()
        return True

    def Delete(self, user: User) -> bool:
        self.session.delete(user)
        self.session.commit()
        return True

    def DeleteById(self, user_id: int) -> bool:
        user = self.GetById(user_id)
        self.Delete(user)
        return True


UserRepositoryDep = Annotated[UserRepository, Depends(UserRepository)]
