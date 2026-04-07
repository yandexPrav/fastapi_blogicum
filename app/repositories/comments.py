"""Comment repository."""

from sqlalchemy.orm import Session

from app import models


class CommentRepository:
    """Repository for comment CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, post_id: int | None = None, skip: int = 0, limit: int = 50):
        query = self.db.query(models.Comment)
        if post_id is not None:
            query = query.filter(models.Comment.post_id == post_id)
        return query.order_by(models.Comment.created_at).offset(skip).limit(limit).all()

    def get_by_id(self, comment_id: int):
        return (
            self.db.query(models.Comment)
            .filter(models.Comment.id == comment_id)
            .first()
        )

    def create(self, payload):
        comment = models.Comment(**payload)
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def update(self, comment: models.Comment, payload):
        for field, value in payload.items():
            setattr(comment, field, value)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def delete(self, comment: models.Comment):
        self.db.delete(comment)
        self.db.commit()

