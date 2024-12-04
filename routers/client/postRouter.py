from fastapi import APIRouter, HTTPException, Query, status

from Database.services.postServices import PostServiceDep
from core.enums import UserRoles
from middlewares.authMiddlewares import protected_route
from viewmodels.requests.client.PostsFilter import PostsFilter
from viewmodels.requests.client.UpdatePostRequest import UpdaetPostRequest
from viewmodels.requests.client.CreatePostRequest import CreatePostRequest
from datetime import date

router = APIRouter()


@router.get("/")
async def getPosts(
    postServices: PostServiceDep,
    keyword: str = None,
    author: str = None,
    startDate: date = None,
    endDate: date = None,
    tags: str = None,
    page: int = 1,
    pageSize: int = 10,
):
    filter = PostsFilter(
        keyword=keyword,
        author=author,
        startDate=startDate,
        endDate=endDate,
        tags=tags.split(",") if tags else None,
    )
    result = await postServices.GetPosts(filter, page, pageSize)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"]
        )

    return result

@router.get("/{id}")
async def getPost(id: int, postServices: PostServiceDep):
    result = await postServices.GetPost(id)

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"]
        )

    return result

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


@router.delete("/{id}")
async def deletePost(
    id: int,
    postServices: PostServiceDep,
    authUser: dict = protected_route([UserRoles.AUTHOR, UserRoles.ADMIN]),
):
    result = await postServices.deletePost(
        id, authUser["Id"] if authUser["Role"] == UserRoles.AUTHOR else None
    )

    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"]
        )

    return result
