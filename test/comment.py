import datetime

from sqlalchemy.orm import subqueryload

from app.database import SessionLocal
from app.models.CommentModel import Comment
from app.models.UserModel import User


# a = [{'time': datetime.datetime(2023, 3, 1, 19, 34, 54)}, {'time': datetime.datetime(2022, 3, 1, 19, 34, 54)}]
#
# sorted_a = sorted(a, key=lambda x: x['time'])
#
# print(sorted_a)
#

def getcommentsbypostid(post_id):
    db = SessionLocal()
    try:
        commentinfo = db.query(Comment).options(subqueryload(Comment.user).load_only(User.username, User.avatar)).all()

        # data = db.query(Comment).options(subqueryload(Comment.user).load_only(User.username, User.avatar)).all()
        # commentlist = db.query(Comment).filter_by(post_id=post_id).options(
        #     subqueryload(Comment.user).load_only(User.username)).first()
        print(commentinfo)
    finally:
        db.close()


if __name__ == '__main__':
    getcommentsbypostid(1)
