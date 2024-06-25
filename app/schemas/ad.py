from pydantic import BaseModel, Field


class TagBase(BaseModel):
    title: str
    description: str | None = None


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    class Config:
        from_attributes = True


class AdBase(BaseModel):
    title: str
    thumb: str | None = None
    owner_id: int
    description: str | None = None
    status: bool = True
    tags: list[Tag] = []


class AdCreate(AdBase):
    pass


class Ad(AdBase):
    id: int

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    ad_id: int
    owner_id: int
    content: str


class CommentCreate(CommentBase):
    content: str = Field(min_length=100, max_length=300)


class Comment(CommentBase):
    id: int

    class Config:
        from_attributes = True
