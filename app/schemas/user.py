from pydantic import BaseModel, Field, ConfigDict


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: str


class UserCreate(UserBase):
    password: str = Field(min_length=10, max_length=100)


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    hashed_password: str

