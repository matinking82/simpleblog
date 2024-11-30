from Database.services.repositories.postRepository import PostRepositoryDep
from Database.services.repositories.tagRepository import TagRepositoryDep
from Database.services.repositories.tagPostRepository import TagPostRepositoryDep
from Database.models.post import Post
from sqlmodel import select
from typing import Annotated
from fastapi import Depends


class PostServices:
    def __init__(
        self,
        postRepository: PostRepositoryDep,
        tagRepository: TagRepositoryDep,
        tagPostRepository: TagPostRepositoryDep,
    ):
        self.adminRepository = postRepository
        self.tagRepository = tagRepository
        self.tagPostRepository = tagPostRepository


PostServiceDep = Annotated[PostServices, Depends(PostServices)]
