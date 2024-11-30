from fastapi import Depends
from typing import Annotated
from sqlmodel import select

from Database.context.context import SessionDep
from Database.models.admin import Admin


class AdminRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def Create(self, admin: Admin):
        self.session.add(admin)
        self.session.commit()

    def GetById(self, admin_id):
        return self.session.exec(select(Admin).where(Admin.id == admin_id)).first()

    def GetByUsername(self, username):
        return self.session.exec(
            select(Admin).where(Admin.username == username)
        ).first()

    def GetAll(self, page=1, pageSize=100, filter=None):
        return self.session.exec(
            select(Admin).limit(pageSize).offset((page - 1) * pageSize).filter(filter)
        ).all()

    def Update(self, admin: Admin):
        self.session.merge(admin)
        self.session.commit()

    def Delete(self, admin: Admin):
        self.session.delete(admin)
        self.session.commit()

    def DeleteById(self, admin_id: int):
        admin = self.GetById(admin_id)
        self.Delete(admin)


AdminRepositoryDep = Annotated[AdminRepository, Depends(AdminRepository)]
