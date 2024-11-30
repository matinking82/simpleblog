from fastapi import Depends
from typing import Annotated
from sqlmodel import select

from Database.context.context import SessionDep
from Database.models.tagPost import TagPost


class TagPostRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def Create(self, tag_post: TagPost):
        self.session.add(tag_post)
        self.session.commit()

    def GetById(self, tag_post_id):
        return self.session.exec(
            select(TagPost).where(TagPost.id == tag_post_id)
        ).first()

    def GetByPostId(self, post_id):
        return self.session.exec(select(TagPost).where(TagPost.postId == post_id)).all()

    def GetByTagId(self, tag_id):
        return self.session.exec(select(TagPost).where(TagPost.tagId == tag_id)).all()

    def GetAll(self, page=1, pageSize=100, filter=None):
        return self.session.exec(
            select(TagPost).limit(pageSize).offset((page - 1) * pageSize).filter(filter)
        ).all()

    def Update(self, tag_post: TagPost):
        self.session.merge(tag_post)
        self.session.commit()

    def Delete(self, tag_post: TagPost):
        self.session.delete(tag_post)
        self.session.commit()

    def DeleteById(self, tag_post_id: int):
        tag_post = self.GetById(tag_post_id)
        self.Delete(tag_post)


TagPostRepositoryDep = Annotated[TagPostRepository, Depends(TagPostRepository)]
