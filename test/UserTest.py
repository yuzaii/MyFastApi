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


def getuseronly():
    db = SessionLocal()
    try:
        user = db.query(User).all()
        print(user)
    finally:
        db.close()


if __name__ == '__main__':
    # create_user()
    create_user('ascasf','dasdas')
