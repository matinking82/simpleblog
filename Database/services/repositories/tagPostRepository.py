from fastapi import Depends
from typing import Annotated
from sqlmodel import select

from Database.context.context import SessionDep
from Database.models.tagPost import TagPost


class TagPostRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def Create(self, tag_post: TagPost) -> bool:
        try:
            self.session.add(tag_post)
            self.session.commit()
            return True
        except:
            return False

    def GetById(self, tag_post_id) -> TagPost:
        return self.session.exec(
            select(TagPost).where(TagPost.id == tag_post_id)
        ).first()

    def GetByPostId(self, post_id) -> list[TagPost]:
        return self.session.exec(select(TagPost).where(TagPost.postId == post_id)).all()

    def GetByTagId(self, tag_id) -> list[TagPost]:
        return self.session.exec(select(TagPost).where(TagPost.tagId == tag_id)).all()

    def GetAll(self, page=1, pageSize=100, filter=None) -> list[TagPost]:
        return self.session.exec(
            select(TagPost).limit(pageSize).offset((page - 1) * pageSize).filter(filter)
        ).all()

    def Update(self, tag_post: TagPost) -> bool:
        try:
            self.session.merge(tag_post)
            self.session.commit()
            return True
        except:
            return False

    def Delete(self, tag_post: TagPost) -> bool:
        try:
            self.session.delete(tag_post)
            self.session.commit()
            return True
        except:
            return False

    def DeleteById(self, tag_post_id: int) -> bool:
        tag_post = self.GetById(tag_post_id)
        if tag_post:
            return self.Delete(tag_post)
        return False


TagPostRepositoryDep = Annotated[TagPostRepository, Depends(TagPostRepository)]