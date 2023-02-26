import logging
from typing import List

import sqlalchemy
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from app.api.UserApi import UserRouter
from app.config import LOGGING_CONFIG, logger
from app.database import Base, engine
from app.models.UserModel import User

# docs_url=None, redoc_url=None 禁用自带的docs文档接口
app = FastAPI(docs_url=None, redoc_url=None)
# 因为下面要用到接口静态文件，所以，这里挂载一下
app.mount('/static', StaticFiles(directory='static'))
app.mount('/img', StaticFiles(directory='upload/img'))


# 利用fastapi提供的函数，生成文档网页
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger/swagger-ui.css")


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc/redoc.standalone.js")


# 允许下列地址跨域
origins = [
    # "*",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5050",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(UserRouter)


# 将首页重定向
@app.get("/", include_in_schema=False)
def index():
    # 日志
    # print(logger)
    # for logger_name in logging.Logger.manager.loggerDict:
    #     print(logger_name)
    logger.info('有人访问api页面')
    return RedirectResponse("/docs")


if __name__ == '__main__':
    # 自动创建数据库
    Base.metadata.create_all(bind=engine)
    # 运行程序
    uvicorn.run(
        app='main:app',
        reload=True,
        port=6060,
        # log_config="logging.yaml",
        log_config=LOGGING_CONFIG
    )
