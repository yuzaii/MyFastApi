#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yuzai
@file:UserSchemas.py
@time:2023/02/22
"""
import datetime
from typing import Optional, Any

from pydantic import BaseModel, validator


class UserBase(BaseModel):
    # Option是可选的 默认为none 唯一性约束
    # id: Optional[int] = Field(None, unique=True)
    user_id: Optional[int]
    username: Optional[str]
    password: Optional[str]


class UserLoginBase(BaseModel):
    username: str
    password: str
    # grant_type: Optional[str] = "password"


# 换成json
# class OAuth2PasswordRequestJSON(BaseModel):
#     username: str
#     password: str

class UserInfo(BaseModel):
    username: str
    sex: Optional[str]
    avatar: Optional[str]
    signature: Optional[str]
    createtime: Any

    @validator('createtime')
    def time_str(cls, v):
        return str(v)


class UserRegisterBase(BaseModel):
    """
    注册时候的json数据
    """
    username: str
    password: str
    secondPassword: str
    # createtime: datetime.datetime.now()


class EditUserBase(BaseModel):
    """
    修改用户信息的
    """
    username: str
    sex: str
    signature: Optional[str]
    newavatar: Optional[str]


class Userchangepass(BaseModel):
    """
    用户修改密码
    """
    oldPassword: str
    firstPassword: str
    secondPassword: str

    # @validator('secondPassword')
    # def eq_password(cls,v):
    #     if
