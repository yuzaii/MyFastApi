from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.GoodsCategoryModel import GoodsCategory

GoodsRouter = APIRouter(prefix='/goods', tags=['商品相关api'])


@GoodsRouter.get('/goods_catetory', summary='获取商品分类信息')
def goods_catetory(db: Session = Depends(get_db)):
    goodscatetory = db.query(GoodsCategory).all()
    # print(goodscatetory)
    return {'code': 200, 'msg': 'success', 'data': goodscatetory}
