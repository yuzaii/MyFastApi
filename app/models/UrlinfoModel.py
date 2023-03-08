from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship

from app.database import Base


class Urlinfo(Base):
    __tablename__ = 'urlinfo'

    url_id = Column(Integer, primary_key=True, autoincrement=True, comment="链接id")
    url_name = Column(String(255), comment='链接名称')
    url = Column(String(255), comment='链接地址')
    url_description = Column(String(255), comment='链接描述')
    tags = Column(String(255), comment='链接标签')
    create_time = Column(DateTime, comment='创建时间')
    update_time = Column(DateTime, comment='更新时间')
    type = Column(SmallInteger, comment='链接类型 0是校内 1是校外')
    user_id = Column(Integer, ForeignKey('user.user_id'), comment='用户id')
    state = Column(SmallInteger, comment='链接状态 0是待审核 1是审核通过')
    user = relationship('User', back_populates='urlinfos')

    def __repr__(self):
        """
        返回字典
        :return:
        """
        return str(self.__dict__)
