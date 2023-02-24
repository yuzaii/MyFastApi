from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.Utils.JwtTools import create_access_token
from app.Utils.auth import oauth2_scheme, auth_depend
from app.Utils.EncryptTools import sha256_encrypt
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
# def login(user: UserLoginBase, db: Session = Depends(get_db)):
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    登录成功之后会返回一个token和一些用户信息
    :param form_data:
    :param db:
    :return:
    """
    print(form_data.username)
    print(form_data.password)
    # return {"access_token": form_data.username, }
    # 判断用户是否存在于数据库中
    db_user = db.query(User).filter_by(username=form_data.username, password=sha256_encrypt(form_data.password)).first()
    # print(user)
    # # 这个可以用聚合函数等等
    # # db_user = db.query(User).filter(
    # #     User.username == user.username and User.password == sha256_encrypt(user.password)).first()
    # # 这个比较方便但不可以进行复杂函数
    # db_user = db.query(User).filter_by(username=user.username, password=sha256_encrypt(user.password)).first()
    print(db_user)
    # 如过存在就生成token 不存在就返回错误信息
    if db_user:
        token = create_access_token({'id': db_user.id, 'username': db_user.username})
        return {'code': 20000, "access_token": token, 'msg': 'success',
                'data': {'id': db_user.id, 'username': db_user.username}}
    else:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
        # return {'code': 20001, 'msg': '用户名或密码不正确'}


@UserRouter.post("/get_all_users_count", summary='获取用户数量')
def get_all_users_count(db: Session = Depends(get_db), data=Depends(auth_depend)):
    print(data)
    count = db.query(User).count()
    return {'count': count, 'code': 20001, 'msg': 'success'}
