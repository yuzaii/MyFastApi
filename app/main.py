from typing import List

import sqlalchemy
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.curd import create_user
from app.database import get_db, Base, engine
from app.models import User
from app.schemas import UserResponse, UserBase, UserListResponse, UserCountResponse, UserInfoResponse

app = FastAPI()


# class UserAlreadyExistsError(Exception):
#     def __init__(self, message="User already exists"):
#         self.message = message
#         super().__init__(self.message)


@app.get("/", tags=['重定向'])
def index():
    return RedirectResponse("/docs")


@app.post("/create_user_depend/", tags=['用户操作'])
def create_user_depend(user: UserBase, db: Session = Depends(get_db)):
    """
    这是一个 FastAPI 框架中常用的依赖注入方式，
    使用 Depends 装饰器注入一个名为 db 的数据库会话对象到 create_user 函数中，
    同时传入一个名为 user 的 UserBase 模型。
    没必要用模型定义
    :param user:
    :param db:
    :return:
    """
    try:
        user = User(name=user.name, email=user.email)
        db.add(user)
        db.commit()
        db.refresh(user)
        return {'msg': 'succuess', 'data': user}
    except:
        # print(e.args)
        db.rollback()
        return {'code': 400, 'msg': 'error'}


@app.post("/create_user_dbsession/", response_model=UserResponse, tags=['用户操作'])
def create_user_dbsession(user: UserBase):
    """
    :param user:

    :return:
    """
    print(123)
    user = User(name=user.name, email=user.email)
    # create_user(user.name,user.email)

    return create_user(user.name, user.email)


@app.post("/get_all_users", response_model=List[UserListResponse], tags=['用户操作'])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    for user in users:
        print(user)
    return users
    # return [UserListResponse.from_orm(user) for user in users]


@app.post("/get_all_users_count", response_model=UserCountResponse, tags=['用户操作'])
def get_all_users_count(db: Session = Depends(get_db)):
    count = db.query(User).count()
    return {'count': count}


@app.post("/get_all_users_info", response_model=UserInfoResponse, tags=['用户操作'])
def get_all_users_count(db: Session = Depends(get_db)):
    # count = db.query(User).count()
    users = db.query(User).all()
    user_list = [UserBase(id=user.id, name=user.name, email=user.email) for user in users]
    count = len(user_list)
    return {"count": count, "users": user_list}


@app.post("/update_eamil", response_model=UserResponse, tags=['用户操作'])
def update_eamil(user_id: int, email: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.email = email
    db.commit()
    db.refresh(db_user)
    return db_user


if __name__ == '__main__':
    # 自动创建数据库
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app='main:app', reload=True)
