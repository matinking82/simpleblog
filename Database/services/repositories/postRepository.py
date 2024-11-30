from fastapi import Depends
from typing import Annotated
from sqlmodel import select

from Database.context.context import SessionDep
from Database.models.post import Post


class PostRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def Create(self, post: Post):
        self.session.add(post)
        self.session.commit()

    def GetById(self, post_id: int):
        return self.session.exec(select(Post).where(Post.id == post_id)).first()

    def GetByAuthorId(self, author_id: int):
        return self.session.exec(select(Post).where(Post.authorId == author_id)).all()

    def GetAll(self, page=1, pageSize=100, filter=None):
        return self.session.exec(
            select(Post).limit(pageSize).offset((page - 1) * pageSize).filter(filter)
        ).all()

    def Update(self, post: Post):
        self.session.merge(post)
        self.session.commit()

    def Delete(self, post: Post):
        self.session.delete(post)
        self.session.commit()
    
    def DeleteById(self, post_id: int):
        post = self.GetById(post_id)
        self.Delete(post)


PostRepositoryDep = Annotated[PostRepository, Depends(PostRepository)]
