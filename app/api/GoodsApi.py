import datetime
import os
import time

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session, load_only, subqueryload

from app.Utils.auth import auth_depend
from app.database import get_db
from app.models.GoodsCategoryModel import GoodsCategory
from app.models.GoodsModel import Goods
from app.models.UserModel import User
from app.schemas.GoodsSchemas import GetGoodsQuery, SearchGoodsQuery, PublishGoods

GoodsRouter = APIRouter(prefix='/goods', tags=['商品相关api'])


@GoodsRouter.get('/goods_catetory', summary='获取商品分类信息')
def goods_catetory(db: Session = Depends(get_db)):
    goodscatetory = db.query(GoodsCategory).all()
    # print(goodscatetory)
    return {'code': 200, 'msg': 'success', 'data': goodscatetory}


@GoodsRouter.post('/getgoods', summary='获取所有商品详细,带id和不带id')
def get_goods(goodsquery: GetGoodsQuery, db: Session = Depends(get_db)):
    print(goodsquery)
    if goodsquery.category_id:
        # 有id
        goods_list = db.query(Goods).filter(Goods.goods_category_id == goodsquery.category_id).options(
            load_only(Goods.goods_name, Goods.goods_detail, Goods.goods_price, Goods.goods_images)).order_by(
            Goods.create_time.desc()).all()
        # print(goods_list)
        return {'code': 200, 'msg': 'success', 'data': goods_list}
    else:
        goods_list = db.query(Goods).options(
            load_only(Goods.goods_name, Goods.goods_detail, Goods.goods_price, Goods.goods_images)).order_by(
            Goods.create_time.desc()).all()
        # print(goods_list)
        return {'code': 200, 'msg': 'success', 'data': goods_list}
    # if goodsquery.categroy_id:
    #     goods_list = db.query(Goods).all()
    #     print('有id')
    #     return {'code': 200, 'msg': 'success', 'data': goods_list}
    # else:
    #     print('无id')
    # return {'code': 200, 'msg': 'success', 'data': goods_list}


@GoodsRouter.post('/searchgoods', summary='搜索所有商品')
def search_goods(goodsquery: SearchGoodsQuery, db: Session = Depends(get_db)):
    print(goodsquery)
    goods_list = db.query(Goods).filter(Goods.goods_name.like(f'%{goodsquery.keyName}%')).options(
        load_only(Goods.goods_name, Goods.goods_detail, Goods.goods_price, Goods.goods_images)).order_by(
        Goods.create_time.desc()).all()
    return {'code': 200, 'msg': 'success', 'data': goods_list}


@GoodsRouter.post("/image/upload", summary='上传商品图片')
async def userimgupload(file: UploadFile = File(...), user=Depends(auth_depend)):
    print('userimgupload')
    # 利用用户id和用时间戳秒来为头像重新命名
    user_id = user.user_id
    # 获取原来的图片格式
    extension = os.path.splitext(file.filename)[1]
    new_filename = f"{user_id}-{int(time.time())}{extension}"

    file.filename = new_filename
    print('新的filename:', file.filename)
    # 将文件上传到upload文件夹中
    contents = await file.read()
    with open(f"./upload/img/goods/{file.filename}", "wb") as f:
        f.write(contents)
    # 这里只负责上传文件 操作数据库需要用户点击确认
    # 上传成功之后将新的文件名保存到数据库中
    # db_user = db.query(User).filter_by(user_id=user_id).first()
    # db_user.avatar = new_filename
    # db.commit()
    # db.refresh(db_user)
    return {'code': 200, 'msg': 'success', 'data': {'filename': new_filename}}


@GoodsRouter.post("/publishgoods", summary='上传商品')
def publish_goods(goods: PublishGoods, db: Session = Depends(get_db), user=Depends(auth_depend)):
    print(user)
    goodsName: str
    goodsDetail: str
    goodsImages: str
    goodsPrice: float
    goodsCategoryId: int
    goodsCount: int
    db_goods = Goods(user_id=user.user_id, goods_name=goods.goodsName, goods_detail=goods.goodsDetail,
                     goods_images=goods.goodsImages,
                     goods_price=goods.goodsPrice, goods_category_id=goods.goodsCategoryId,
                     goods_count=goods.goodsCount, create_time=datetime.datetime.now(), goods_status=0, view_num=0)
    db.add(db_goods)
    db.commit()
    db.refresh(db_goods)
    return {'code': 200, 'msg': 'success', 'data': {'good_id': db_goods.goods_id}}


@GoodsRouter.get("/getgoodsbyid", summary='根据商品id获取商品信息')
def getgoods_byid(good_id: int, db: Session = Depends(get_db)):
    goodinfo = db.query(Goods).filter(Goods.goods_id == good_id).options(
        subqueryload(Goods.user).load_only(User.username, User.avatar, User.signature)).options(
        subqueryload(Goods.goods_category).load_only(GoodsCategory.category_name)).first()
    goodinfo.view_num += 1
    db.commit()
    db.refresh(goodinfo)

    return {'code': 200, 'msg': 'success', 'data': goodinfo}
