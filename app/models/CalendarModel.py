from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, SmallInteger, Date
from sqlalchemy.orm import relationship

from app.database import Base


class Calendar(Base):
    __tablename__ = 'calendar'

    date_id = Column(Integer, primary_key=True, autoincrement=True, comment="日期id")
    date_name = Column(String(255), comment='日期名称')
    date = Column(Date, comment='日期地址')
    # date_description = Column(String(255), comment='日期描述')
    # tags = Column(String(255), comment='日期标签')
    create_time = Column(DateTime, comment='创建时间')
    update_time = Column(DateTime, comment='更新时间')
    # type = Column(SmallInteger, comment='日期类型 0是校内 1是校外')
    user_id = Column(Integer, ForeignKey('user.user_id'), comment='用户id')
    state = Column(SmallInteger, comment='日期状态 0是待审核 1是审核通过')
    user = relationship('User', back_populates='calendars')

    def __repr__(self):
        """
        返回字典
        :return:
        """
        return str(self.__dict__)
