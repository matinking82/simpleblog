from Database.services.repositories.commentsRepository import CommentRepositoryDep
from Database.models.comment import Comment
from sqlmodel import select
from typing import Annotated
from fastapi import Depends


class CommentServices:
    def __init__(self, commentRepository: CommentRepositoryDep):
        self.adminRepository = commentRepository


CommentServiceDep = Annotated[CommentServices, Depends(CommentServices)]