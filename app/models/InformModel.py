from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, SmallInteger, Text, Date
from sqlalchemy.orm import relationship

from app.database import Base


class Inform(Base):
    __tablename__ = 'inform'

    inform_id = Column(Integer, primary_key=True, autoincrement=True, comment="通知id")
    inform_title = Column(String(255), comment='通知标题')
    inform_detail = Column(Text, comment='通知详情')
    inform_date = Column(Date, comment='发布通知的日期')
    create_time = Column(DateTime, comment='创建时间')
    update_time = Column(DateTime, comment='更新时间')
    type = Column(SmallInteger, comment='链接类型 1是校内 2是大赛 3是其他')
    user_id = Column(Integer, ForeignKey('user.user_id'), comment='用户id')
    state = Column(SmallInteger, comment='链接状态 0是待审核 1是审核通过')
    user = relationship('User', back_populates='informs')

    def __repr__(self):
        """
        返回字典
        :return:
        """
        return str(self.__dict__)
