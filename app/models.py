"""SQLAlchemy models based on Django blogicum models (up to sprint 8)."""

from datetime import datetime

from sqlalchemy import (
    Boolean, Column, DateTime, ForeignKey, Integer, String, Text
)
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """User model (replaces Django's built-in User)."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    email = Column(String(254), unique=True, index=True, nullable=False)
    first_name = Column(String(150), default="")
    last_name = Column(String(150), default="")
    bio = Column(Text, default="")
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime, default=datetime.utcnow)

    posts = relationship("Post", back_populates="author",
                         foreign_keys="Post.author_id")
    comments = relationship("Comment", back_populates="author")


class Category(Base):
    """Category model — corresponds to Django Category(PublishedModel)."""

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    slug = Column(String(50), unique=True, index=True, nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    posts = relationship("Post", back_populates="category")


class Location(Base):
    """Location model — corresponds to Django Location(PublishedModel)."""

    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    posts = relationship("Post", back_populates="location")


class Post(Base):
    """Post model — corresponds to Django Post(PublishedModel)."""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), nullable=False)
    text = Column(Text, nullable=False)
    pub_date = Column(DateTime, nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    image = Column(String(255), default="", nullable=True)

    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    author = relationship("User", back_populates="posts",
                          foreign_keys=[author_id])
    location = relationship("Location", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )


class Comment(Base):
    """Comment model — corresponds to Django Comment."""

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
