from fastapi import Depends
from typing import Annotated
from sqlmodel import select

from Database.context.context import SessionDep
from Database.models.tag import Tag


class TagRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def Create(self, tag: Tag) -> bool:
        try:
            self.session.add(tag)
            self.session.commit()
            return True
        except:
            return False

    def GetById(self, tag_id) -> Tag:
        return self.session.exec(select(Tag).where(Tag.id == tag_id)).first()

    def GetByName(self, name) -> Tag:
        return self.session.exec(
            select(Tag).where(Tag.name == name)
        ).first()

    def GetAll(self, page=1, pageSize=100, filter=None) -> list[Tag]:
        return self.session.exec(
            select(Tag).limit(pageSize).offset((page - 1) * pageSize).filter(filter)
        ).all()

    def Update(self, tag: Tag) -> bool:
        try:
            self.session.merge(tag)
            self.session.commit()
            return True
        except:
            return False

    def Delete(self, tag: Tag) -> bool:
        try:
            self.session.delete(tag)
            self.session.commit()
            return True
        except:
            return False

    def DeleteById(self, tag_id: int) -> bool:
        tag = self.GetById(tag_id)
        if tag:
            return self.Delete(tag)
        return False


TagRepositoryDep = Annotated[TagRepository, Depends(TagRepository)]
