import logging
import sys
from typing import Dict, Any

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
    # jwt_exp_seconds: int = 60 * 60 * 2
    jwt_exp_seconds: int = 60 * 60 * 2
    # jwt_exp_seconds: int = 1


settings = Settings()

"""
日志相关
"""

LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s---%(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(asctime)s---%(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
            "use_colors": True,
        },
        "file": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(levelprefix)s %(asctime)s---%(client_addr)s - "%(request_line)s" %(status_code)s',
            "use_colors": False,
        }
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "file",
            "filename": "../log/myapp.log",
            "maxBytes": 10485760,
            "backupCount": 5
        },
        "defaultfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": "../log/myapp.log",
            "maxBytes": 10485760,
            "backupCount": 5
        }
    },
    "loggers": {
        "uvicorn": {"handlers": ["default", "defaultfile"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access", "file"], "level": "INFO", "propagate": False},
    },
}
logger = logging.getLogger("uvicorn")
# logger.info('123123')
