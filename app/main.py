import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.curd import create_user
from app.database import get_db
from app.models import User
from app.schemas import UserResponse, UserBase

app = FastAPI()


@app.get("/")
def index():
    return RedirectResponse("/docs")


@app.post("/create_user_depend/", response_model=UserResponse)
def create_user_depend(user: UserBase, db: Session = Depends(get_db)):
    """
    这是一个 FastAPI 框架中常用的依赖注入方式，
    使用 Depends 装饰器注入一个名为 db 的数据库会话对象到 create_user 函数中，
    同时传入一个名为 user 的 UserBase 模型。
    :param user:
    :param db:
    :return:
    """
    print(123)
    user = User(name=user.name, email=user.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/create_user_dbsession/", response_model=UserResponse)
def create_user_dbsession(user: UserBase):
    """
    :param user:

    :return:
    """
    print(123)
    user = User(name=user.name, email=user.email)
    # create_user(user.name,user.email)

    return create_user(user.name, user.email)


if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)
