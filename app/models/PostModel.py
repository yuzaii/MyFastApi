from sqlalchemy import Column, Integer, String, Boolean, Date, Time, DateTime, Text, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship

from app.database import Base


class Post(Base):
    __tablename__ = "post"

    post_id = Column(Integer, primary_key=True, index=True, comment='帖子id')
    title = Column(String(50), comment='标题')
    detail = Column(Text, comment='内容')
    images = Column(String(200), comment='图片列表')
    comment_num = Column(Integer, comment='评论数')
    view_num = Column(Integer, comment='点击数')
    create_time = Column(DateTime, comment='创建时间')
    user_id = Column(Integer, ForeignKey('user.user_id'))
    category_id = Column(SmallInteger, ForeignKey('post_category.category_id'), comment='种类id')
    update_time = Column(DateTime, comment='更新时间')
    best_post = Column(SmallInteger, comment='用户id')
    collect_num = Column(Integer, comment='点击数')
    post_status = Column(SmallInteger, comment='帖子状态')
    # overlaps = "user"
    user = relationship('User', viewonly=True)

    # postcategory = relationship('PostCategory', viewonly=True)

    def __repr__(self):
        """
        返回字典
        :return:
        """
        return str(self.__dict__)
