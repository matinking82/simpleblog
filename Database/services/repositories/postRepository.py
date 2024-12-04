from fastapi import Depends
from typing import Annotated
from sqlmodel import select

from Database.context.context import SessionDep
from Database.models.post import Post


import logging

from Database.models.tag import Tag
from Database.models.tagPost import TagPost
from Database.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PostRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def Create(self, post: Post) -> bool:
        try:
            self.session.add(post)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def GetById(self, post_id: int) -> Post:
        return self.session.exec(select(Post).where(Post.id == post_id)).first()

    def GetByAuthorId(self, author_id: int) -> list[Post]:
        return self.session.exec(select(Post).where(Post.authorId == author_id)).all()

    def GetAll(self, page=1, pageSize=100, filter=True) -> list[Post]:
        return self.session.exec(
            select(Post).limit(pageSize).offset((page - 1) * pageSize).filter(filter)
        ).all()

    def Update(self, post: Post) -> bool:
        try:
            self.session.merge(post)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def Delete(self, post: Post) -> bool:
        try:
            self.session.delete(post)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def DeleteById(self, post_id: int) -> bool:
        post = self.GetById(post_id)
        if post:
            return self.Delete(post)
        return False


PostRepositoryDep = Annotated[PostRepository, Depends(PostRepository)]
