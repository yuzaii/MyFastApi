#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yuzai
@file:CommentModel.py
@time:2023/03/01
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from app.database import Base


class Comment(Base):
    __tablename__ = 'comment'
    comment_id = Column(Integer, primary_key=True, index=True, comment='评论id')
    text = Column(String(100), comment='评论内容')
    images = Column(String(200), comment='评论图片')
    post_id = Column(Integer, ForeignKey('post.post_id'), comment='帖子id')
    user_id = Column(Integer, ForeignKey('user.user_id'), comment='用户id')
    parent_id = Column(Integer, comment='父评论id')
    create_time = Column(DateTime, comment='创建时间')

    def __repr__(self):
        """
        返回字典
        :return:
        """
        return str(self.__dict__)
