import sys

# print(sys.platform)
# 对自己不同电脑的数据库链接
if sys.platform == 'darwin':
    SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:20000526@localhost:3306/fastapi'
else:
    SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:Zly20000526.@192.168.10.17:3306/NTUTOOLS'
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_MAX_OVERFLOW = 10
