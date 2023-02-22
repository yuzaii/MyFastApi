from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.UserModel import User
from app.schemas.UserSchemas import UserBase

UserRouter = APIRouter(prefix='/user', tags=['用户注册'])


# api全部小写

@UserRouter.post("/register", summary='用户注册')
def Register(user: UserBase, db: Session = Depends(get_db)):
    try:
        db_user = User(name=user.name, password=user.password)
        print(db_user)
        # TODO这里需要将密码加密
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        print(db_user)
        return {'code': 200, 'msg': 'succuess', 'data': db_user}
    except Exception as e:
        db.rollback()
        return {'code': 400, 'msg': 'error', 'detail': str(e.__cause__)}


@UserRouter.post("/login", summary='用户登录')
def Login(user: UserBase, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.name == user.name, User.password == user.password).first()
    print(db_user)
    if db_user:
        return {'code': 20000, 'msg': 'succuess', 'data': {'id': user.id, 'name': user.name}}
    else:
        return {'code': 20001, 'msg': '用户名或密码不正确'}


@UserRouter.post("/get_all_users_count", summary='获取用户数量')
def get_all_users_count(db: Session = Depends(get_db)):
    count = db.query(User).count()
    return {'count': count, 'code': 20001, 'msg': '用户名或密码不正确'}
