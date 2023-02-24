from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from flask_sqlalchemy.session import Session
from jose import jwt, JWTError
from starlette import status

from app.config import settings
from app.database import get_db
from app.models.UserModel import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


def auth_depend(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    对token进行解码
    :param token:
    :param db:
    :return:
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except (jwt.ExpiredSignatureError, JWTError):
        raise HTTPException(
            status_code=201,
            detail="token已失效，请重新登陆！",
            # headers={"WWW-Authenticate": "Bearer"}
        )
    print('payload', payload)
    # 获取数据库中的
    db_user = db.query(User).filter_by(id=payload.get('id')).first()
    print('db_user', db_user)
    if db_user:
        return db_user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="认证不通过",
            # headers={"WWW-Authenticate": "Bearer"}
        )

# async def auth_depend1(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
#     print('token:', token)
#     # 对token解码
#     user = decode_token(token)
#     db_user=db_user = db.query(User).filter_by(id=user.get('id')).first()
#     print(db_user)
#     if token != '123':
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="you are not 123",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return 'This is data'
