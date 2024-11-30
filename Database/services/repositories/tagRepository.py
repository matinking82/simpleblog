from fastapi import Depends
from typing import Annotated
from sqlmodel import select

from Database.context.context import SessionDep
from Database.models.tag import Tag


class TagRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def Create(self, tag: Tag):
        self.session.add(tag)
        self.session.commit()

    def GetById(self, tag_id):
        return self.session.exec(select(Tag).where(Tag.id == tag_id)).first()

    def GetByName(self, name):
        return self.session.exec(
            select(Tag).where(Tag.name == name)
        ).first()

    def GetAll(self, page=1, pageSize=100, filter=None):
        return self.session.exec(
            select(Tag).limit(pageSize).offset((page - 1) * pageSize).filter(filter)
        ).all()

    def Update(self, tag: Tag):
        self.session.merge(tag)
        self.session.commit()

    def Delete(self, tag: Tag):
        self.session.delete(tag)
        self.session.commit()

    def DeleteById(self, tag_id: int):
        tag = self.GetById(tag_id)
        self.Delete(tag)


TagRepositoryDep = Annotated[TagRepository, Depends(TagRepository)]
