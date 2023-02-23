from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.Utils.encrypt import sha256_encrypt
from app.database import get_db
from app.models.UserModel import User
from app.schemas.UserSchemas import UserLoginBase, UserRegisterBase

UserRouter = APIRouter(prefix='/user', tags=['用户注册'])


# api全部小写

@UserRouter.post("/register", summary='用户注册')
def register(user: UserRegisterBase, db: Session = Depends(get_db)):
    print(user)
    if user.password != user.secondPassword:
        return {'code': 20001, 'msg': '两次输入密码不一致'}
    try:
        exit_user = db.query(User).filter_by(username=user.username).first()
        if exit_user:
            return {'code': 20001, 'msg': '该用户名已被占用'}
        db_user = User(username=user.username, password=sha256_encrypt(user.password))
        print(db_user)
        # TODO这里需要将密码加密
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        print(db_user)
        return {'code': 20000, 'msg': '账号创建成功'}
    except Exception as e:
        db.rollback()
        return {'code': 20001, 'msg': str(e)}


@UserRouter.post("/login", summary='用户登录')
def login(user: UserLoginBase, db: Session = Depends(get_db)):
    print(user)
    # 这个可以用聚合函数等等
    # db_user = db.query(User).filter(
    #     User.username == user.username and User.password == sha256_encrypt(user.password)).first()
    # 这个比较方便但不可以进行复杂函数
    db_user = db.query(User).filter_by(username=user.username, password=sha256_encrypt(user.password)).first()
    print(db_user)
    if db_user:
        return {'code': 20000, 'msg': 'succuess', 'data': {'id': db_user.id, 'username': user.username}}
    else:
        return {'code': 20001, 'msg': '用户名或密码不正确'}


@UserRouter.post("/get_all_users_count", summary='获取用户数量')
def get_all_users_count(db: Session = Depends(get_db)):
    count = db.query(User).count()
    return {'count': count, 'code': 20001, 'msg': '用户名或密码不正确'}
