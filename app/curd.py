from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db, SessionLocal
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





if __name__ == '__main__':
    create_user('12113', '123')

