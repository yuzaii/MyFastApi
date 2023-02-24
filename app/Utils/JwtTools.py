from datetime import timedelta, datetime

from fastapi import HTTPException, Depends
from flask_sqlalchemy.session import Session
from jose import jwt, JWTError
from starlette import status

from app.config import settings
from app.database import get_db
from app.models.UserModel import User


# 生成token
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    print(data)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=settings.jwt_exp_seconds)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt



if __name__ == '__main__':
    # user = User(id=1, username='123').__dict__
    # print(user.__dict__)
    # user = {'id': 1, 'username': '123'}
    # token1 = create_access_token(user)
    # print(token1)
    token1 = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTAsInVzZXJuYW1lIjoiMTIzIiwiZXhwIjoxNjc3MjYxNDc1fQ.SdKEe_D4uMHuscPTYN34fwr2znVuT9S3vKTHsafYg-A'
    # user = decode_token(token1)
    # print(user)
    # print(type(user))
