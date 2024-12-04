from fastapi import Depends
from typing import Annotated
from sqlmodel import select

from Database.context.context import SessionDep
from Database.models.tag import Tag
from Database.models.tagPost import TagPost

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TagPostRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def Create(self, tag_post: TagPost) -> bool:
        try:
            self.session.add(tag_post)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def GetById(self, tag_post_id) -> TagPost:
        return self.session.exec(
            select(TagPost).where(TagPost.id == tag_post_id)
        ).first()

    def GetByPostId(self, post_id) -> list[TagPost]:
        return self.session.exec(select(TagPost).where(TagPost.postId == post_id)).all()

    def GetByTagId(self, tag_id) -> list[TagPost]:
        return self.session.exec(select(TagPost).where(TagPost.tagId == tag_id)).all()

    def GetTagNamesByPostId(self, post_id) -> list[str]:
        join = self.session.exec(
            select(TagPost, Tag)
            .where(TagPost.tagId == Tag.id)
            .where(TagPost.postId == post_id)
        ).all()

        return [j[1].name for j in join]

    def DeleteByPostId(self, post_id) -> bool:
        try:
            tagposts = self.GetByPostId(post_id)
            for tagpost in tagposts:
                self.session.delete(tagpost)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def GetAll(self, page=1, pageSize=100, filter=True) -> list[TagPost]:
        return self.session.exec(
            select(TagPost).limit(pageSize).offset((page - 1) * pageSize).filter(filter)
        ).all()

    def Update(self, tag_post: TagPost) -> bool:
        try:
            self.session.merge(tag_post)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def Delete(self, tag_post: TagPost) -> bool:
        try:
            self.session.delete(tag_post)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def DeleteById(self, tag_post_id: int) -> bool:
        tag_post = self.GetById(tag_post_id)
        if tag_post:
            return self.Delete(tag_post)
        return False


TagPostRepositoryDep = Annotated[TagPostRepository, Depends(TagPostRepository)]
