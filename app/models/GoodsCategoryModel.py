from sqlalchemy import Column, Integer, String, Boolean, Date, Time, DateTime, SmallInteger
from sqlalchemy.orm import relationship

from app.database import Base


class GoodsCategory(Base):
    __tablename__ = "goods_category"
    category_id = Column(Integer, primary_key=True, index=True, comment='种类id')
    category_level = Column(SmallInteger, comment='种类等级')
    parent_id = Column(Integer, comment='父类的种类id')
    category_name = Column(String(50), comment='种类名称')
    create_time = Column(DateTime, comment='创建时间')
    update_time = Column(DateTime, comment='更新时间')

    # posts = relationship('Post', back_populates='post_category')

    def __repr__(self):
        """
        返回字典
        :return:
        """
        return str(self.__dict__)
