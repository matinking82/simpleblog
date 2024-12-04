from Database.services.repositories.commentsRepository import CommentRepositoryDep
from Database.models.comment import Comment
from sqlmodel import select
from typing import Annotated
from fastapi import Depends
from datetime import datetime

from Database.services.repositories.userRepository import UserRepositoryDep
from viewmodels.requests.client.CreateCommentRequest import CreateCommentRequest
from viewmodels.responses.client.CommentViewModel import CommentViewModel


class CommentServices:
    def __init__(
        self, commentRepository: CommentRepositoryDep, userRepository: UserRepositoryDep
    ):
        self.commentRepository = commentRepository
        self.userRepository = userRepository

    async def createComment(
        self, postId: int, authorId: int, request: CreateCommentRequest
    ):
        comment = Comment(
            postId=postId,
            readerId=authorId,
            content=request.content,
            created_at=datetime.now(),
        )
        success = self.commentRepository.Create(comment)
        if not success:
            return {"success": False, "message": "failed to create comment"}
        return {"success": True, "message": "comment created successfully"}

    async def getCommentsForPost(self, postId: int):
        comments = self.commentRepository.GetByPostId(postId)

        if not comments:
            return {"success": False, "message": "something went wrong"}

        result: list[CommentViewModel] = []

        for comment in comments:
            reader = self.userRepository.GetById(comment.readerId)
            if not reader:
                return {"success": False, "message": "something went wrong"}

            result.append(
                CommentViewModel(
                    id=comment.id,
                    content=comment.content,
                    created_at=comment.created_at,
                    reader=reader.username,
                    postId=comment.postId,
                    readerId=comment.readerId,
                )
            )

        return {"success": True, "comments": result}


CommentServiceDep = Annotated[CommentServices, Depends(CommentServices)]
