from fastapi import Depends
from typing import Annotated
from sqlmodel import select

from Database.context.context import SessionDep
from Database.models.comment import Comment


class CommentRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def Create(self, comment: Comment):
        self.session.add(comment)
        self.session.commit()

    def GetById(self, comment_id):
        return self.session.exec(
            select(Comment).where(Comment.id == comment_id)
        ).first()

    def GetAll(self, page=1, pageSize=100, filter=None):
        return self.session.exec(
            select(Comment).limit(pageSize).offset((page - 1) * pageSize).filter(filter)
        ).all()

    def GetByPostId(self, post_id):
        return self.session.exec(select(Comment).where(Comment.postId == post_id)).all()

    def GetByAuthorId(self, author_id):
        return self.session.exec(
            select(Comment).where(Comment.authorId == author_id)
        ).all()

    def Update(self, comment: Comment):
        self.session.merge(comment)
        self.session.commit()

    def Delete(self, comment: Comment):
        self.session.delete(comment)
        self.session.commit()

    def DeleteById(self, comment_id: int):
        comment = self.GetById(comment_id)
        self.Delete(comment)


CommentRepositoryDep = Annotated[CommentRepository, Depends(CommentRepository)]
