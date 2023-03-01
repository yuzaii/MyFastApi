from sqlalchemy.orm import load_only, subqueryload

from app.Utils.Pagination import Pagination
from app.database import SessionLocal
from app.models.CommentModel import Comment
from app.models.PostModel import Post
from app.models.UserModel import User


def create_user(name: str, password: str):
    db = SessionLocal()
    try:
        print('asds')
        db_user = User(name=name, password=password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    finally:
        db.close()


def create_post():
    db = SessionLocal()
    db_post = Post(title='如何学习fastapi', detail='如何学习fastapi')
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    db.close()


def getpostbyid(user_id):
    db = SessionLocal()
    # 查询这个用户的所有帖子
    user = db.query(User).filter_by(user_id=user_id).first()
    # 直接获取到这个用户 因为定义了关联表 所以post就可以找到
    print(user.posts)
    # for post in user.posts:
    #     print(post)

    # 查询id1用户 title是123的贴子
    # results = db.query(User, Post).filter(User.user_id == Post.user_id).all()
    # for result in results:
    #     print(result)

    db.close()


def getpostbypostid(post_id):
    db = SessionLocal()
    # 帖子的用户名称
    # post = db.query(Post).filter_by(post_id=post_id).first()
    # # 直接获取到这个用户 因为定义了关联表 所以post就可以找到 但是比较麻烦
    # print(post)
    # print(post.user)
    # filter_by 和 filter都可以
    # post_info = db.query(Post, User.username).filter_by(
    #     post_id=post_id).join(User, User.user_id == Post.user_id).first()

    post_info = db.query(Post, User.username).join(User, User.user_id == Post.user_id).all()
    print(post_info)
    print(type(post_info))


def getpost():
    db = SessionLocal()
    try:
        category_id = 1
        # title = 'java'
        title = ''
        pageNum = 10
        pageSize = 1
        # 如果有
        if title:
            postlist = db.query(Post).filter_by(category_id=1).filter(Post.title.like(f'%{title}%')).all()
            # postlist = db.query(Post).filter_by(category_id=2,).all()
            print(postlist)
            for post in postlist:
                print(post)
        else:
            post_query = db.query(Post).filter_by(category_id=1)
            print(post_query)
            print(type(post_query))
            # postlist = db.query(Post).filter_by(category_id=1)
            # postlist=Pagination(pageNum, pageSize, error_out=False)
            postlist, total = Pagination(post_query, pageNum, pageSize).paginate()
            # print(postlist)

            print(len(postlist))
            print(f"总数", total)
            print('每个数据')
            for post in postlist:
                print(post)
        return
    finally:
        db.close()


def getpostandusername():
    db = SessionLocal()
    try:
        pageNum = 1
        pageSize = 10
        # post_query = db.query(Post, User.username).filter_by(category_id=1).join(User, User.user_id == Post.user_id)
        # # print(post_query)
        # datas, total = Pagination(post_query, pageNum, pageSize).paginate()
        # print(len(datas))
        # postlist = []
        # for data in datas:
        #     postinfo = data[0].__dict__
        #     postinfo['username'] = data[1]
        #     postlist.append(postinfo)
        # print(postlist)
        # 优化一
        # post_query = db.query(Post, User.username).select_from(Post).join(User).filter(Post.category_id == 1).all()
        # print(post_query)
        # postlist = [data[0].__dict__ for data in post_query]
        # 优化二
        # post_query = db.query(Post, User.username).select_from(Post).join(User).filter(Post.category_id == 1)
        # postdata, total = Pagination(post_query, pageNum, pageSize).paginate()
        # # print(postdata)
        # postlist = [p._asdict() for p in postdata]
        # print(postlist[0])
        # for i in postlist:
        #     print(i)
        # options(
        # db.load_only(Post, User.username)).all()
        # 可以用啊
        # d = db.query(Post).options(load_only(Post.post_id)).all()
        # d = db.query(Post).options(load_only(Post.post_id)).all()
        # print(d)
        # dd = db.query(Post, User.username).select_from(Post).join(User).filter(Post.category_id == 1).options(
        #     load_only(Post.post_id)).first()
        # print(dd)
        # postlist = [p._asdict() for p in db.query(Post, User.username)
        # .select_from(Post)
        # .join(User)
        # .filter(Post.category_id == 1)
        # .options(load_only(Post.post_id, User.username))
        # .all()]

        # print(postdata)
        # post_query = db.query(Post, User.username).select_from(Post).join(User).filter(
        #     Post.category_id == getpostinfo.category_id).order_by(Post.create_time.desc())
        # 继续优化
        # data = db.query(Comment).options(subqueryload(Comment.user).load_only(User.username, User.avatar)).all()
        post_query = db.query(Post).filter_by(category_id=1).options(subqueryload(Post.user).load_only(User.username))
        postdata, total = Pagination(post_query, pageNum, pageSize).paginate()
        print(postdata)
        print(total)
    finally:
        db.close()


if __name__ == '__main__':
    # create_user('12113', '123')
    # getpost(1)
    # getpost()
    # getpostbypostid(10)
    getpostandusername()
