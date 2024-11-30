from Database.services.repositories.postRepository import PostRepositoryDep
from Database.models.post import Post
from sqlmodel import select
from typing import Annotated
from fastapi import Depends



class postServices:
    def __init__(self, postRepository: PostRepositoryDep):
        self.adminRepository = postRepository


PostServiceDep = Annotated[postServices, Depends(postServices)]
