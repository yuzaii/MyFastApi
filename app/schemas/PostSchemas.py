from typing import Optional

from pydantic import BaseModel, validator


class PublisPost(BaseModel):
    title: str
    detail: str
    images: Optional[str]
    category_id: int

    @validator('images')
    def imgnull(cls, v):
        if v == '':
            return None
