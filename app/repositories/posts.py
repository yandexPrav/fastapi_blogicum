"""Post repository."""

from sqlalchemy.orm import Session, joinedload

from app import models


class PostRepository:
    """Repository for post CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 20, published_only: bool = False):
        query = self.db.query(models.Post)
        if published_only:
            query = query.filter(models.Post.is_published.is_(True))
        return query.order_by(models.Post.pub_date.desc()).offset(skip).limit(limit).all()

    def get_by_id(self, post_id: int):
        return self.db.query(models.Post).filter(models.Post.id == post_id).first()

    def get_detailed_by_id(self, post_id: int):
        return (
            self.db.query(models.Post)
            .options(
                joinedload(models.Post.author),
                joinedload(models.Post.category),
                joinedload(models.Post.location),
                joinedload(models.Post.comments),
            )
            .filter(models.Post.id == post_id)
            .first()
        )

    def create(self, payload):
        post = models.Post(**payload)
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def update(self, post: models.Post, payload):
        for field, value in payload.items():
            setattr(post, field, value)
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete(self, post: models.Post):
        self.db.delete(post)
        self.db.commit()

