"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


# ─────────────────────────────── User ────────────────────────────────────────

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str = ""
    last_name: str = ""
    bio: str = ""


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    email: Optional[EmailStr] = None


class UserOut(UserBase):
    id: int
    is_active: bool
    date_joined: datetime

    class Config:
        from_attributes = True


# ─────────────────────────────── Category ────────────────────────────────────

class CategoryBase(BaseModel):
    title: str
    description: str
    slug: str
    is_published: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    is_published: Optional[bool] = None


class CategoryOut(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ─────────────────────────────── Location ────────────────────────────────────

class LocationBase(BaseModel):
    name: str
    is_published: bool = True


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    is_published: Optional[bool] = None


class LocationOut(LocationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ─────────────────────────────── Post ────────────────────────────────────────

class PostBase(BaseModel):
    title: str
    text: str
    pub_date: datetime
    is_published: bool = True
    image: Optional[str] = None
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    is_published: Optional[bool] = None
    image: Optional[str] = None
    location_id: Optional[int] = None
    category_id: Optional[int] = None


class PostOut(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PostDetail(PostOut):
    author: UserOut
    category: Optional[CategoryOut] = None
    location: Optional[LocationOut] = None
    comments: List["CommentOut"] = []

    class Config:
        from_attributes = True


# ─────────────────────────────── Comment ─────────────────────────────────────

class CommentBase(BaseModel):
    text: str
    post_id: int
    author_id: int


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    text: Optional[str] = None


class CommentOut(CommentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Resolve forward reference
PostDetail.model_rebuild()
