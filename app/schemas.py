"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, field_validator


# ─────────────────────────────── User ────────────────────────────────────────

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str = ""
    last_name: str = ""
    bio: str = ""

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 3:
            raise ValueError("username должен содержать минимум 3 символа")
        if " " in value:
            raise ValueError("username не должен содержать пробелы")
        return value


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("password должен содержать минимум 8 символов")
        return value


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

    @field_validator("title", "description")
    @classmethod
    def validate_text_fields(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("поле не может быть пустым")
        return value.strip()

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, value: str) -> str:
        allowed = "abcdefghijklmnopqrstuvwxyz0123456789-_"
        cleaned = value.strip().lower()
        if not cleaned:
            raise ValueError("slug не может быть пустым")
        if any(ch not in allowed for ch in cleaned):
            raise ValueError("slug может содержать только [a-z0-9-_]")
        return cleaned


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

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name не может быть пустым")
        return value.strip()


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

    @field_validator("title", "text")
    @classmethod
    def validate_post_text_fields(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("поле не может быть пустым")
        return value.strip()


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

    @field_validator("text")
    @classmethod
    def validate_comment_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text комментария не может быть пустым")
        return value.strip()


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
