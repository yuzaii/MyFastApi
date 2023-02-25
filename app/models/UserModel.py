from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, Time, DateTime

from app.database import Base


class User(Base):
    """
    id：一个整数类型的主键，表示用户的唯一 ID。
    name：一个字符串类型的字段，表示用户的名字。
    email：一个字符串类型的字段，表示用户的电子邮件地址。
    在这个例子中，我们指定了这个字段为唯一的，并创建了一个索引，以便我们可以更快地查询用户的电子邮件地址。
    注意：
    这里的String(255)并不是varchar(255)
    能确定的话最好把string的长度降低
    """
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True, comment='用户ID')
    username = Column(String(50), unique=True, comment='用户名')
    password = Column(String(100), comment='密码')
    role_id = Column(Integer, comment='角色id')
    sex = Column(String(2), comment='性别')
    locked = Column(Integer, comment='是否被锁定')
    avatar = Column(String(100), comment='头像')
    signature = Column(String(100), comment='个性签名')
    createtime = Column(DateTime, comment='创建时间')
    updatetime = Column(DateTime, comment='更新时间')
    lastlogintime = Column(DateTime, comment='上一次登录时间')

    def __repr__(self):
        return f'<User user_id:{self.user_id},username:{self.username},password:{self.password}' \
               f' createtime:{self.createtime}>'
