"""Post repository."""

from sqlalchemy.orm import Session, joinedload

from app import models
from app.repositories.utils import db_call


class PostRepository:
    """Repository for post CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 20, published_only: bool = False):
        def _get_all():
            query = self.db.query(models.Post)
            if published_only:
                query = query.filter(models.Post.is_published.is_(True))
            return query.order_by(models.Post.pub_date.desc()).offset(skip).limit(limit).all()

        return db_call("posts.get_all", _get_all)

    def get_by_id(self, post_id: int):
        return db_call(
            "posts.get_by_id",
            lambda: self.db.query(models.Post).filter(models.Post.id == post_id).first(),
        )

    def get_detailed_by_id(self, post_id: int):
        return db_call(
            "posts.get_detailed_by_id",
            lambda: self.db.query(models.Post)
            .options(
                joinedload(models.Post.author),
                joinedload(models.Post.category),
                joinedload(models.Post.location),
                joinedload(models.Post.comments),
            )
            .filter(models.Post.id == post_id)
            .first(),
        )

    def create(self, payload):
        def _create():
            post = models.Post(**payload)
            self.db.add(post)
            self.db.commit()
            self.db.refresh(post)
            return post

        return db_call("posts.create", _create)

    def update(self, post: models.Post, payload):
        def _update():
            for field, value in payload.items():
                setattr(post, field, value)
            self.db.commit()
            self.db.refresh(post)
            return post

        return db_call("posts.update", _update)

    def delete(self, post: models.Post):
        return db_call("posts.delete", lambda: (self.db.delete(post), self.db.commit()))

