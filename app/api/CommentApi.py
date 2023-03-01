#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yuzai
@file:CommentApi.py
@time:2023/03/01
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.CommentModel import Comment

CommentRouter = APIRouter(prefix='/comment', tags=['论坛评论相关api'])


@CommentRouter.get("/getcommnetsbypostid", summary="根据文章id获取评论信息")
def getcommnets(post_id: int, db: Session = Depends(get_db)):
    commentinfo = db.query(Comment).filter_by(post_id=post_id).all()
    return commentinfo
