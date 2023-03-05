from typing import Optional

from pydantic import BaseModel


class GetGoodsQuery(BaseModel):
    category_id: Optional[int]


class SearchGoodsQuery(BaseModel):
    keyName: Optional[str]


class PublishGoods(BaseModel):
    goodsName: str
    goodsDetail: str
    goodsImages: str
    goodsPrice: float
    goodsCategoryId: int
    goodsCount: int
