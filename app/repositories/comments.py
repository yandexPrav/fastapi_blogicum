"""Comment repository."""

from sqlalchemy.orm import Session

from app import models
from app.repositories.utils import db_call


class CommentRepository:
    """Repository for comment CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, post_id: int | None = None, skip: int = 0, limit: int = 50):
        def _get_all():
            query = self.db.query(models.Comment)
            if post_id is not None:
                query = query.filter(models.Comment.post_id == post_id)
            return query.order_by(models.Comment.created_at).offset(skip).limit(limit).all()

        return db_call("comments.get_all", _get_all)

    def get_by_id(self, comment_id: int):
        return db_call(
            "comments.get_by_id",
            lambda: self.db.query(models.Comment)
            .filter(models.Comment.id == comment_id)
            .first(),
        )

    def create(self, payload):
        def _create():
            comment = models.Comment(**payload)
            self.db.add(comment)
            self.db.commit()
            self.db.refresh(comment)
            return comment

        return db_call("comments.create", _create)

    def update(self, comment: models.Comment, payload):
        def _update():
            for field, value in payload.items():
                setattr(comment, field, value)
            self.db.commit()
            self.db.refresh(comment)
            return comment

        return db_call("comments.update", _update)

    def delete(self, comment: models.Comment):
        return db_call(
            "comments.delete",
            lambda: (self.db.delete(comment), self.db.commit()),
        )

