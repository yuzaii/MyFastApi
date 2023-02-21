from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.curd import create_user
from app.database import get_db
from app.models.UserModel import User
from app.schemas import UserInfoResponse, UserBase, UserResponse, UserListResponse, UserCountResponse

UserRouter = APIRouter(prefix='/User', tags=['用户操作'])


@UserRouter.post("/create_user_depend/", summary='依赖注入方法创建用户')
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
        user = User(name=user.name, password=user.password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return {'msg': 'succuess', 'data': user}
    except Exception as e:
        # print(e.args)
        db.rollback()
        return {'code': 400, 'msg': 'error', 'detail': str(e.__cause__)}
        # return {'code': 400, 'msg': 'error', 'detail': str(e.__context__)}
        # return {'code': 400, 'msg': 'error', 'detail': str(e.)}


@UserRouter.post("/create_user_dbsession/", response_model=UserResponse, summary='普通方法创建用户')
def create_user_dbsession(user: UserBase):
    """
    :param user:
    :return:
    """
    print(123)
    user = User(name=user.name, password=user.password)
    # create_user(user.name,user.password)

    return create_user(user.name, user.password)


@UserRouter.post("/get_all_users", response_model=List[UserListResponse], summary='获取所有用户信息,没有code，count等')
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    for user in users:
        print(user)
    return users
    # return [UserListResponse.from_orm(user) for user in users]


@UserRouter.post("/get_all_users_info", response_model=UserInfoResponse, summary="获取用户详细信息,带code和count信息")
def get_all_users_count(db: Session = Depends(get_db)):
    # count = db.query(User).count()
    users = db.query(User).all()
    for u in users:
        print(u)
    user_list = [UserBase(id=user.id, name=user.name, password=user.password) for user in users]
    count = len(user_list)
    return {"code": 200, "count": count, "data": user_list}


@UserRouter.post("/get_all_users_count", response_model=UserCountResponse, summary='获取用户数量')
def get_all_users_count(db: Session = Depends(get_db)):
    count = db.query(User).count()
    return {'count': count}


@UserRouter.post("/update_password", response_model=UserResponse, tags=['用户操作'], summary='修改用户密码')
def update_password(user_id: int, password: str, db: Session = Depends(get_db)):
    # 先找到再修改
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    # 直接在找到的地方改
    db_user.password = password
    db.commit()
    db.refresh(db_user)
    return db_user


@UserRouter.post("/delete_user", tags=['用户操作'], summary="删除用户")
def delete_user(id: int, db: Session = Depends(get_db)):
    # user = db.query(User).filter(User.id == id).first()
    # user = db.query(User).filter_by(id=id).first()
    # print('user', user)
    # print(123)
    try:
        # 先找到对象再删除1
        # user = db.query(User).filter_by(id=id).first()
        # 先找到对象再删除2
        user = db.query(User).filter(User.id == id).first()
        # 确定唯一用这个 但是如果存在不唯一或为空就会异常
        # user = db.query(User).filter(User.id == id).one()
        print(user)
        if not user:
            return {'code': 400, 'msg': 'User not found'}
        db.delete(user)
        db.commit()
        # 也可以直接这么写 但是直接删除会导致不存在的也会不会报错
        # db.query(User).filter(User.id == id).delete()
        # db.commit()
        return {'code': 200, 'msg': 'succuess'}
    except Exception as e:
        db.rollback()
        return {'code': 400, 'msg': 'error', 'detail': str(e.__cause__)}
