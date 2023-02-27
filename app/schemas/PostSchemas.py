from typing import Optional

from pydantic import BaseModel, validator


class PublisPostBase(BaseModel):
    title: str
    detail: str
    images: Optional[str]
    category_id: int

    @validator('images')
    def imgnull(cls, v):
        if v == '':
            return None


class GetPostBase(BaseModel):
    category_id: Optional[int]
    # title: Optional[str]
    pageNum: int
    pageSize: int
