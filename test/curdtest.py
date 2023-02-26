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


def getpost(user_id):
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


if __name__ == '__main__':
    # create_user('12113', '123')
    getpost(1)
