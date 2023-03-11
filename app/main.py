import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from app.api.CalendarApi import CalendarApi
from app.api.CommentApi import CommentRouter
from app.api.GoodsApi import GoodsRouter
from app.api.InformApi import InformApi
from app.api.PostApi import PostRouter
from app.api.UrlApi import UrlRouter
from app.api.UserApi import UserRouter
from app.config import LOGGING_CONFIG, logger
from app.database import engine, Base
from app.models.CommentModel import Comment
from app.models.CalendarModel import Calendar
from app.models.GoodsCategoryModel import GoodsCategory
from app.models.GoodsModel import Goods
from app.models.InformModel import Inform
from app.models.PostCategoryModel import PostCategory
from app.models.PostModel import Post
from app.models.UrlinfoModel import Urlinfo
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
        swagger_css_url="/static/swagger/swagger-ui.css",
        swagger_ui_parameters={"docExpansion": None},
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc/redoc.standalone.js")


# 允许下列地址跨域
origins = [
    "*",
    # "http://192.168.10.10:5050"
    # "http://localhost",
    # "http://localhost:8080",
    # "http://localhost:5050",
    # "http://127.0.0.1:5500",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 挂载路由
app.include_router(UserRouter)
app.include_router(PostRouter)
app.include_router(CommentRouter)
app.include_router(GoodsRouter)
app.include_router(UrlRouter)
app.include_router(CalendarApi)
app.include_router(InformApi)


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
    models = [User, Post, PostCategory, Comment, GoodsCategory, Goods, Urlinfo, Calendar, Inform]
    tables = [model.__table__ for model in models]
    Base.metadata.create_all(bind=engine, tables=tables)
    print('Uvicorn running on http://127.0.0.1:6060')
    # 运行程序
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        reload=True,
        port=6060,
        # log_config="logging.yaml",
        log_config=LOGGING_CONFIG
    )
