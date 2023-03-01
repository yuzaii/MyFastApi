from sqlalchemy import Column, Integer, String, Boolean, Date, Time, DateTime, SmallInteger
from sqlalchemy.orm import relationship

from app.database import Base


class PostCategory(Base):
    __tablename__ = "post_category"
    category_id = Column(Integer, primary_key=True, index=True, comment='种类id')
    category_name = Column(String(50), unique=True, comment='种类名')
    description = Column(String(100), comment='种类描述')

    posts = relationship('Post', back_populates='post_category')

    def __repr__(self):
        """
        返回字典
        :return:
        """
        return str(self.__dict__)
