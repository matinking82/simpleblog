from Database.models.tag import Tag
from Database.models.tagPost import TagPost
from Database.services.repositories.postRepository import PostRepositoryDep
from Database.services.repositories.tagRepository import TagRepositoryDep
from Database.services.repositories.tagPostRepository import TagPostRepositoryDep
from Database.models.post import Post
from sqlmodel import select
from typing import Annotated
from fastapi import Depends
from datetime import datetime

from Database.services.repositories.userRepository import UserRepositoryDep
from viewmodels.requests.client.CreatePostRequest import CreatePostRequest
from viewmodels.requests.client.PostsFilter import PostsFilter
from viewmodels.requests.client.UpdatePostRequest import UpdaetPostRequest
from viewmodels.responses.client.PostViewModel import PostViewModel


class PostServices:
    def __init__(
        self,
        postRepository: PostRepositoryDep,
        tagRepository: TagRepositoryDep,
        tagPostRepository: TagPostRepositoryDep,
        userRepository: UserRepositoryDep,
    ):
        self.tagRepository = tagRepository
        self.tagPostRepository = tagPostRepository
        self.postRepository = postRepository
        self.userRepository = userRepository

    async def userCreatePost(self, authorId: int, request: CreatePostRequest):
        author = self.userRepository.GetById(authorId)
        if not author:
            return {"success": False, "message": "author not found"}

        now = datetime.now()
        post = Post(
            title=request.title,
            content=request.content,
            authorId=authorId,
            created_at=now,
            updated_at=now,
        )
        success = self.postRepository.Create(post)
        if not success:
            return {"success": False, "message": "failed to create post"}

        for tag in request.tags:
            tagmodel = self.tagRepository.GetByName(tag)

            if not tagmodel:
                tagmodel = Tag(name=tag)
                success = self.tagRepository.Create(tagmodel)

                if not success:
                    return {"success": False, "message": "failed to create tag"}

            success = self.tagPostRepository.Create(
                TagPost(tagId=tagmodel.id, postId=post.id)
            )

            if not success:
                return {"success": False, "message": "failed to create tagpost"}

        return {
            "success": True,
            "message": "post created",
            "post": PostViewModel(
                id=post.id,
                title=post.title,
                content=post.content,
                authorId=post.authorId,
                author=None if not author else author.username,
                created_at=post.created_at,
                updated_at=post.updated_at,
                tags=request.tags,
            ),
        }

    async def adminCreatePost(self, request: CreatePostRequest):
        now = datetime.now()
        post = Post(
            title=request.title,
            content=request.content,
            created_at=now,
            updated_at=now,
        )
        success = self.postRepository.Create(post)

        if not success:
            return {"success": False, "message": "failed to create post"}

        for tag in request.tags:
            tagmodel = self.tagRepository.GetByName(tag)

            if not tagmodel:
                tagmodel = Tag(name=tag)
                success = self.tagRepository.Create(tagmodel)

                if not success:
                    return {"success": False, "message": "failed to create tag"}

            success = self.tagPostRepository.Create(
                TagPost(tagId=tagmodel.id, postId=post.id)
            )

            if not success:
                return {"success": False, "message": "failed to create tagpost"}

        return {
            "success": True,
            "message": "post created",
            "post": PostViewModel(
                id=post.id,
                title=post.title,
                content=post.content,
                authorId=None,
                author=None,
                created_at=post.created_at,
                updated_at=post.updated_at,
                tags=request.tags,
            ),
        }

    async def updatePost(
        self, id: int, request: UpdaetPostRequest, authorId: int | None = None
    ):
        post = self.postRepository.GetById(id)

        if not post:
            return {"success": False, "message": "post not found"}

        if authorId and post.authorId != authorId:
            return {"success": False, "message": "unauthorized"}

        post.title = request.title if request.title else post.title
        post.content = request.content if request.content else post.content

        post.updated_at = datetime.now()

        success = self.postRepository.Update(post)

        if not success:
            return {"success": False, "message": "failed to update post"}
        tags: list[str] = []
        if request.tags:
            success = self.tagPostRepository.DeleteByPostId(post.id)
            if not success:
                return {"success": False, "message": "failed to delete tags"}
            tags = request.tags
            for tag in request.tags:
                tagmodel = self.tagRepository.GetByName(tag)

                if not tagmodel:
                    tagmodel = Tag(name=tag)
                    success = self.tagRepository.Create(tagmodel)

                    if not success:
                        return {"success": False, "message": "failed to create tag"}

                success = self.tagPostRepository.Create(
                    TagPost(tagId=tagmodel.id, postId=post.id)
                )

                if not success:
                    return {"success": False, "message": "failed to create tagpost"}
        else:
            tags = self.tagPostRepository.GetTagNamesByPostId(post.id)

        return {
            "success": True,
            "message": "post updated",
            "post": PostViewModel(
                id=post.id,
                title=post.title,
                content=post.content,
                authorId=post.authorId,
                author=(
                    None
                    if not post.authorId
                    else self.userRepository.GetById(post.authorId).username
                ),
                created_at=post.created_at,
                updated_at=post.updated_at,
                tags=tags,
            ),
        }

    async def deletePost(self, id: int, authorId: int | None = None):
        post = self.postRepository.GetById(id)

        if not post:
            return {"success": False, "message": "post not found"}

        if authorId and post.authorId != authorId:
            return {"success": False, "message": "unauthorized"}

        success = self.tagPostRepository.DeleteByPostId(post.id)
        if not success:
            return {"success": False, "message": "failed to delete tags"}

        success = self.postRepository.Delete(post)
        if not success:
            return {"success": False, "message": "failed to delete post"}

        return {"success": True, "message": "post deleted"}

    async def GetPosts(
        self, postsFilter: PostsFilter, page: int = 1, pageSize: int = 100
    ):
        filter = True

        # TODO:filter

        posts = self.postRepository.GetAll(page, pageSize, filter)
        postViewModels: list[PostViewModel] = []
        for post in posts:
            tags = self.tagPostRepository.GetTagNamesByPostId(post.id)

            postViewModels.append(
                PostViewModel(
                    id=post.id,
                    title=post.title,
                    content=post.content,
                    authorId=post.authorId,
                    author=(
                        None
                        if not post.authorId
                        else self.userRepository.GetById(post.authorId).username
                    ),
                    created_at=post.created_at,
                    updated_at=post.updated_at,
                    tags=tags,
                )
            )

        return {
            "success": True,
            "message": "posts found",
            "posts": postViewModels,
        }


PostServiceDep = Annotated[PostServices, Depends(PostServices)]
