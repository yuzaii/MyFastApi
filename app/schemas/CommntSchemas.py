#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yuzai
@file:CommntSchemas.py
@time:2023/03/02
"""
from pydantic import BaseModel


class CreateCommnet(BaseModel):
    post_id: int
    text: str


class CommitReply(BaseModel):
    reply_comment_id: int
    text: str


class DeleteComment(BaseModel):
    comment_id: int
