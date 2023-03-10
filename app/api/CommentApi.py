#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:yuzai
@file:CommentApi.py
@time:2023/03/01
"""
import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, subqueryload

from app.Utils.auth import auth_depend
from app.database import get_db
from app.models.CommentModel import Comment
from app.models.PostModel import Post
from app.models.UserModel import User
from app.schemas.CommntSchemas import CreateCommnet, CommitReply, DeleteComment

CommentRouter = APIRouter(prefix='/comment', tags=['论坛评论相关api'])


def generate_parent_commmets(all_comments):
    parent_commmets = []
    # 先挑出主评论
    for comment in all_comments:
        # print(comment.parent_comment_id)
        if comment.parent_comment_id == 0:
            # print(123)
            # 是主评论 添加到需要返回的评论表
            parent_commmets.append(comment)
            # print('添加了')
            # 需不需要删除呢？？？ 不删 目的是为了获取主评论的username
    # 挑出主评论后将commentlist_resp按时间怕排序最后排序
    sorted_commmet_list = sorted(parent_commmets, key=lambda x: x.create_time)
    return sorted_commmet_list


def add_child_commmets(parent_commments, all_comments, comment_user_dict):
    # 遍历主评论追加副评论
    for parent_commmet in parent_commments:
        # 定义一个孩子评论列表
        child_comments = []
        # print(parent_commmet)
        # 遍历所有评论列表 筛选自己的孩子评论
        for child_comment in all_comments:
            if child_comment.parent_comment_id == parent_commmet.comment_id:
                # 如果孩子评论的parent_comment_id和父评论的post_id相同就把他塞进自己的child_comments
                # print('孩子')
                # 获取回复评论的的用户名
                child_comment.reply_user = comment_user_dict.get(child_comment.reply_comment_id)
                child_comments.append(child_comment)
            sorted_child_comments = sorted(child_comments, key=lambda x: x.create_time)
            parent_commmet.child_comments = sorted_child_comments
    return parent_commments


# commentinfo = db.query(Comment).filter_by(post_id=post_id).all()
# a = [{'time': datetime.datetime(2023, 3, 1, 19, 34, 54)}, {'time': datetime.datetime(2022, 3, 1, 19, 34, 54)}]
@CommentRouter.get("/getcommnetsbypostid", summary="根据文章id获取评论信息")
def getcommnets(post_id: int, db: Session = Depends(get_db)):
    # 这里需要获取的信息多且复杂
    # 先获取这个id的所有评论吧
    all_comments = db.query(Comment).filter_by(post_id=post_id).options(
        subqueryload(Comment.user).load_only(User.username, User.avatar)).all()
    # print("一开始从数据库中获取的列表", all_comments)
    print("一个获取到", len(all_comments), "条评论")
    # 将评论变成字典key是comment_id value这条评论者的名字
    comment_user_dict = {obj.comment_id: obj.user for obj in all_comments}
    # print(comment_user_dict)
    # print(commentlist)
    # 先挑出主评论 下面已经排序
    parent_commments = generate_parent_commmets(all_comments)
    commentlist = add_child_commmets(parent_commments, all_comments, comment_user_dict)
    # print(commentlist)

    # print(parent_commmets)
    # print("逐个输出")
    # for i in parent_commmets:
    #     print(i)
    # # print(sorted_commentlist)
    # # print(len(commentlist_resp))
    # print(all_comments)
    return {'code': 200, 'msg': 'success', 'data': {'commentlist': commentlist}}


@CommentRouter.post("/commitcommnet", summary="发表评论")
def commitcommnet(createcommnet: CreateCommnet, db: Session = Depends(get_db), user=Depends(auth_depend)):
    print(createcommnet)
    db_comment = Comment(user_id=user.user_id, post_id=createcommnet.post_id, text=createcommnet.text,
                         parent_comment_id=0, reply_comment_id=0, create_time=datetime.datetime.now())
    db.add(db_comment)
    # db.commit()
    # db.refresh(db_comment)
    print(db_comment)
    # 增加文章评论量
    postinfo = db.query(Post).filter_by(post_id=db_comment.post_id).first()
    postinfo.comment_num += 1
    db.commit()
    # 可以不加
    # db.refresh(postinfo)
    return {'code': 200, 'msg': '评论成功'}


@CommentRouter.post("/commitreply", summary="发表回复")
def commitreply(reply: CommitReply, db: Session = Depends(get_db), user=Depends(auth_depend)):
    # 这里应该获取到的时候需要回复的id 并找到他
    parent_comment = db.query(Comment).filter_by(comment_id=reply.reply_comment_id).first()
    # 获取需要回复的评论的文章id
    post_id = parent_comment.post_id
    # 祖父评论的id
    pp_commmentid = parent_comment.parent_comment_id
    # 如果祖父评论的id是0 说明父亲评论是主评论 如果是0 就是他的评论id 如果不是0就是他的父亲id
    parent_comment_id = parent_comment.comment_id if pp_commmentid == 0 else parent_comment.parent_comment_id
    reply_comment_id = parent_comment.comment_id
    # print('reply_comment_id',reply_comment_id)
    db_comment = Comment(user_id=user.user_id, text=reply.text, post_id=post_id, parent_comment_id=parent_comment_id,
                         reply_comment_id=reply_comment_id, create_time=datetime.datetime.now())
    db.add(db_comment)
    # db.commit()
    # db.refresh(db_comment)
    # 增加文章评论量
    postinfo = db.query(Post).filter_by(post_id=db_comment.post_id).first()
    postinfo.comment_num += 1
    db.commit()
    # 可以不加
    # db.refresh(postinfo)
    return {'code': 200, 'msg': '评论成功'}


@CommentRouter.post("/deletecomment", summary="删除评论")
def deletecomment(comment: DeleteComment, db: Session = Depends(get_db), user=Depends(auth_depend)):
    comment_id = comment.comment_id
    # 删除和自己有关的评论
    row1 = db.query(Comment).filter_by(parent_comment_id=comment_id).delete()
    row2 = db.query(Comment).filter_by(reply_comment_id=comment_id).delete()
    # 删除自己
    row3 = db.query(Comment).filter_by(comment_id=comment_id).delete()
    print(row3, row2, row1)
    # db.commit()
    # 增加文章评论量
    postinfo = db.query(Post).filter_by(post_id=comment.post_id).first()
    postinfo.comment_num -= row3 + row2 + row1
    db.commit()
    # 可以不加
    # db.refresh(postinfo)
    return {'code': 200, 'msg': '删除成功'}
