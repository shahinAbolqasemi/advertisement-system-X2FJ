from pydantic import BaseModel, Field, ConfigDict

from app import models


class TagBase(BaseModel):
    title: str
    description: str | None = None


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class AdBase(BaseModel):
    title: str
    # thumb: str | None = None
    description: str | None = None
    # tags: list[Tag] = []


class AdCreate(AdBase):
    pass


class AdUpdate(BaseModel):
    title: str
    # thumb: str | None = None
    description: str | None = None


class AdPartialUpdate(BaseModel):
    title: str | None = None
    # thumb: str | None = None
    description: str | None = None


class Ad(AdBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    status: models.AdvertiseStatus


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    content: str = Field(min_length=100, max_length=300)


class Comment(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    advertise_id: int
