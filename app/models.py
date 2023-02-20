from sqlalchemy import create_engine, Column, Integer, String, Boolean

from app.database import Base


class User(Base):
    """
    id：一个整数类型的主键，表示用户的唯一 ID。
    name：一个字符串类型的字段，表示用户的名字。
    email：一个字符串类型的字段，表示用户的电子邮件地址。
    在这个例子中，我们指定了这个字段为唯一的，并创建了一个索引，以便我们可以更快地查询用户的电子邮件地址。
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255), unique=True, index=True)

    def __repr__(self):
        return f'<User {self.name}>'
