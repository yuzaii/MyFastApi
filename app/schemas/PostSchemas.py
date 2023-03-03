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
    # 这里要么是category_id为空要么title为空
    category_id: Optional[int]
    # title: Optional[str]
    pageNum: int
    pageSize: int


class SearchBase(BaseModel):
    searchTitle: Optional[str]
    pageNum: int
    pageSize: int
