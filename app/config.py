import sys
from pydantic import BaseSettings

"""
数据库相关设置
"""
# print(sys.platform)
# 对自己不同电脑的数据库链接
if sys.platform == 'darwin':
    SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:20000526@localhost:3306/fastapi'
else:
    SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:Zly20000526.@192.168.10.17:3306/NTUTOOLS'
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_MAX_OVERFLOW = 10

"""
jwt相关配置
"""


class Settings(BaseSettings):
    # jwt加密的key
    jwt_secret_key: str = 'ntutoolsNB'
    # jwt的加密算法
    jwt_algorithm: str = 'HS256'
    # token过期时间 单位秒
    jwt_exp_seconds: int = 60 * 60 * 2
    # jwt_exp_seconds: int = 1


settings = Settings()
