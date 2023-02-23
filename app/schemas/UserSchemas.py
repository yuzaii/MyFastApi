#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yuzai
@file:UserSchemas.py
@time:2023/02/22
"""
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    # Option是可选的 默认为none 唯一性约束
    # id: Optional[int] = Field(None, unique=True)
    id: Optional[int]
    username: Optional[str]
    password: Optional[str]


class UserLoginBase(BaseModel):
    username: str
    password: str


class UserRegisterBase(BaseModel):
    username: str
    password: str
    secondPassword: str
