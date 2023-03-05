from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.mysql import DOUBLE

from app.database import Base


class Goods(Base):
    __tablename__ = 'goods'

    goods_id = Column(Integer, primary_key=True, index=True, comment='二手商品id')
    goods_name = Column(String(255), comment='二手商品名称')
    goods_detail = Column(String(255), comment='二手商品详情')
    goods_images = Column(String(255), comment='二手商品图片')
    goods_price = Column(DOUBLE(10, 2), comment='二手商品定价')
    goods_category_id = Column(Integer, comment='二手商品分类id')
    goods_count = Column(Integer, comment='二手商品数量')
    goods_status = Column(Boolean, comment='二手商品上架状态：0-下架 1-上架')
    create_time = Column(DateTime, comment='二手商品发布时间')
    update_time = Column(DateTime, comment='二手商品信息更新时间')
    user_id = Column(Integer, ForeignKey('user.user_id'), comment='发布人id')
    view_num = Column(Integer, comment='点击数')

    def __repr__(self):
        return str(self.__dict__)
