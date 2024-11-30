from Database.services.repositories.tagRepository import TagRepositoryDep
from Database.models.tag import Tag
from sqlmodel import select
from typing import Annotated
from fastapi import Depends


class tagServices:
    def __init__(self, tagRepository: TagRepositoryDep):
        self.adminRepository = tagRepository


TagServiceDep = Annotated[tagServices, Depends(tagServices)]
