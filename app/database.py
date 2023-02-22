from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from app.config import SQLALCHEMY_DATABASE_URL, SQLALCHEMY_POOL_SIZE, SQLALCHEMY_MAX_OVERFLOW

# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:Zly20000526.@192.168.10.17:3306/NTUTOOLS?pool_size=5&max_overflow=10'

"""
    pool_size: 连接池中维护的连接数量，默认为 5。
    max_overflow: 允许连接池中最多额外创建的连接数，当连接池中的连接都被使用，且达到最大连接数限制时，如果需要再创建新的连接，则会创建一个新的连接，直到创建的连接数量达到 pool_size + max_overflow，默认为 10。
    pool_recycle: 连接池中的连接被回收的时间，超过该时间的连接会被回收，单位是秒，默认为 -1，表示不回收。
    echo: 是否打印执行的 SQL 语句和其他调试信息，默认为 False。
    echo_pool: 是否打印连接池的调试信息，默认为 False。
"""
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       pool_size=SQLALCHEMY_POOL_SIZE,
                       max_overflow=SQLALCHEMY_MAX_OVERFLOW,
                       echo=False,
                       echo_pool=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Session:
    """
    依赖注入的db
    :return:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
