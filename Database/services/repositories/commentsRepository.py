from fastapi import Depends
from typing import Annotated
from sqlmodel import select

from Database.context.context import SessionDep
from Database.models.comment import Comment


import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CommentRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def Create(self, comment: Comment) -> bool:
        try:
            self.session.add(comment)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def GetById(self, comment_id) -> Comment:
        return self.session.exec(
            select(Comment).where(Comment.id == comment_id)
        ).first()

    def GetAll(self, page=1, pageSize=100, filter=True) -> list[Comment]:
        return self.session.exec(
            select(Comment).limit(pageSize).offset((page - 1) * pageSize).filter(filter)
        ).all()

    def GetByPostId(self, post_id) -> list[Comment]:
        try:
            return self.session.exec(
                select(Comment).where(Comment.postId == post_id)
            ).all()
        except Exception as e:
            logger.error(e)
            return None

    def GetByAuthorId(self, author_id) -> list[Comment]:
        return self.session.exec(
            select(Comment).where(Comment.authorId == author_id)
        ).all()

    def Update(self, comment: Comment) -> bool:
        try:
            self.session.merge(comment)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def Delete(self, comment: Comment) -> bool:
        try:
            self.session.delete(comment)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def DeleteById(self, comment_id: int) -> bool:
        comment = self.GetById(comment_id)
        if comment:
            return self.Delete(comment)
        return False


CommentRepositoryDep = Annotated[CommentRepository, Depends(CommentRepository)]
