from fastapi import Depends
from typing import Annotated
from sqlmodel import select

from Database.context.context import SessionDep
from Database.models.admin import Admin

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdminRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def Create(self, admin: Admin) -> bool:
        try:
            self.session.add(admin)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def GetById(self, admin_id) -> Admin:
        return self.session.exec(select(Admin).where(Admin.id == admin_id)).first()

    def GetByUsername(self, username) -> Admin:
        return self.session.exec(
            select(Admin).where(Admin.username == username)
        ).first()

    def GetAll(self, page=1, pageSize=100, filter=True) -> list[Admin]:
        return self.session.exec(
            select(Admin).limit(pageSize).offset((page - 1) * pageSize).filter(filter)
        ).all()

    def Update(self, admin: Admin) -> bool:
        try:
            self.session.merge(admin)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def Delete(self, admin: Admin) -> bool:
        try:
            self.session.delete(admin)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def DeleteById(self, admin_id: int) -> bool:
        admin = self.GetById(admin_id)
        if admin:
            return self.Delete(admin)
        return False


AdminRepositoryDep = Annotated[AdminRepository, Depends(AdminRepository)]
