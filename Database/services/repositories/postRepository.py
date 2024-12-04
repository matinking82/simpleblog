from fastapi import Depends
from typing import Annotated
from sqlmodel import select

from Database.context.context import SessionDep
from Database.models.post import Post


import logging

from Database.models.tag import Tag
from Database.models.tagPost import TagPost
from Database.models.user import User
from viewmodels.requests.client.PostsFilter import PostsFilter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PostRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def Create(self, post: Post) -> bool:
        try:
            self.session.add(post)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def GetById(self, post_id: int) -> Post:
        return self.session.exec(select(Post).where(Post.id == post_id)).first()

    def GetByAuthorId(self, author_id: int) -> list[Post]:
        return self.session.exec(select(Post).where(Post.authorId == author_id)).all()

    def GetAll(self, page=1, pageSize=100, filter: PostsFilter = None):
        # """
        # select post.* from post left outer join user on user.id=post.authorId left outer join tagpost on post.id=tagpost.post
        # Id left outer join tag on tagpost.tagId=tag.id where title like '%%' and content like '%%' and tag.name like '%%' and post.c
        # reated_at>'2024-12-02' and post.created_at<'2024-12-04' and user.username='string2';
        # """
        base_query = (
            select(Post).distinct()
            .outerjoin(User, User.id == Post.authorId)
            .outerjoin(TagPost, TagPost.postId == Post.id)
            .outerjoin(Tag, Tag.id == TagPost.tagId)
        )

        if filter and filter.keyword:
            base_query = base_query.where(
                Post.title.like(f"%{filter.keyword}%")
                | Post.content.like(f"%{filter.keyword}%")
            )
        if filter and filter.author:
            base_query = base_query.where(User.username == filter.author)

        if filter and filter.tags:
            base_query = base_query.where(Tag.name.in_(filter.tags))

        if filter and filter.startDate:
            base_query = base_query.where(Post.created_at >= filter.startDate)

        if filter and filter.endDate:
            base_query = base_query.where(Post.created_at <= filter.endDate)

        base_query = (
            base_query.order_by(Post.id.desc())
            .limit(pageSize)
            .offset((page - 1) * pageSize)
        )

        return self.session.exec(base_query).all()

    def Update(self, post: Post) -> bool:
        try:
            self.session.merge(post)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def Delete(self, post: Post) -> bool:
        try:
            self.session.delete(post)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(e)
            return False

    def DeleteById(self, post_id: int) -> bool:
        post = self.GetById(post_id)
        if post:
            return self.Delete(post)
        return False


PostRepositoryDep = Annotated[PostRepository, Depends(PostRepository)]
