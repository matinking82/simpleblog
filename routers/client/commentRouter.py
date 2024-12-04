from fastapi import APIRouter, HTTPException, status

from Database.services.commentServices import CommentServiceDep
from core.enums import UserRoles
from middlewares.authMiddlewares import protected_route
from viewmodels.requests.client.CreateCommentRequest import CreateCommentRequest

router = APIRouter()


@router.post("/{postId}")
async def createComment(
    postId: int,
    request: CreateCommentRequest,
    commentServices: CommentServiceDep,
    authUser: dict = protected_route([UserRoles.READER]),
):
    result = await commentServices.createComment(postId, authUser["Id"], request)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"]
        )

    return result


@router.get("/{postId}")
async def getComments(
    postId: int,
    commentServices: CommentServiceDep,
):
    result = await commentServices.getCommentsForPost(postId)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"]
        )

    return result
