from app.Utils.Pagination import Pagination
from app.database import SessionLocal
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
            postlist, pages = Pagination(post_query, pageNum, pageSize).paginate()
            # print(postlist)

            print(len(postlist))
            print(f"总页数", pages)
            print('每个数据')
            for post in postlist:
                print(post)
        return
    finally:
        db.close()


if __name__ == '__main__':
    # create_user('12113', '123')
    # getpost(1)
    getpost()
