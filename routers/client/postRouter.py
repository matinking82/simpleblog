from fastapi import APIRouter, HTTPException, status

from Database.services.postServices import PostServiceDep
from core.enums import UserRoles
from middlewares.authMiddlewares import protected_route
from viewmodels.requests.client.UpdatePostRequest import UpdaetPostRequest
from viewmodels.requests.client.CreatePostRequest import CreatePostRequest

router = APIRouter()


@router.post("/")
async def createPost(
    request: CreatePostRequest,
    postServices: PostServiceDep,
    authUser: dict = protected_route([UserRoles.AUTHOR, UserRoles.ADMIN]),
):
    if authUser["Role"] == UserRoles.ADMIN:
        result = await postServices.adminCreatePost(request)
    else:
        result = await postServices.userCreatePost(authUser["Id"], request)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"]
        )

    return result


@router.put("/{id}")
async def updatePost(
    id: int,
    request: UpdaetPostRequest,
    postServices: PostServiceDep,
    authUser: dict = protected_route([UserRoles.AUTHOR, UserRoles.ADMIN]),
):
    result = await postServices.updatePost(
        id, request, authUser["Id"] if authUser["Role"] == UserRoles.AUTHOR else None
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"]
        )

    return result
