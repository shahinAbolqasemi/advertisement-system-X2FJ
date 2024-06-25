from pydantic import BaseModel, Field


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: str


class UserCreate(UserBase):
    password: str = Field(min_length=10, max_length=100)


class User(UserBase):
    id: int
    username: str
    hashed_password: str

    class Config:
        from_attributes = True
