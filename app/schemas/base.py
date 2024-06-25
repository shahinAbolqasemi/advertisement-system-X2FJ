import enum

from pydantic import BaseModel


class ResponseStatus(str, enum.Enum):
    SUCCESS = 'success'
    ERROR = 'error'


class ResponseBase(BaseModel):
    status: ResponseStatus
    message: str | None = None


class StandardResponse(ResponseBase):
    pass


class RetrieveResponse(ResponseBase):
    data: dict | None = None


class ListResponse(ResponseBase):
    data: list[dict] = []
