import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.Utils.auth import auth_depend
from app.database import get_db
from app.models.PostCategoryModel import PostCategory
from app.models.PostModel import Post
from app.schemas.PostSchemas import PublisPostBase, GetPostBase

PostRouter = APIRouter(prefix='/post', tags=['论坛相关api'])


@PostRouter.get("/postcategory", summary="获取帖子种类学信息")
def getpostcategory(db: Session = Depends(get_db)):
    postcategorys = db.query(PostCategory).all()
    # print(postcategorys)
    return {'code': 200, 'msg': 'success', 'data': postcategorys}


@PostRouter.post("/publishpost", summary="发布帖子")
def publishpost(post: PublisPostBase, db: Session = Depends(get_db), user=Depends(auth_depend)):
    # user_id = user.user_id
    print(post)
    # 构造帖子对象
    db_post = Post(user_id=user.user_id, title=post.title, detail=post.detail,
                   images=post.images, comment_num=0, view_num=0, best_post=0,
                   category_id=post.category_id, createtime=datetime.datetime.now(),
                   collect_num=0, post_status=0)
    print(db_post)
    # 将贴子添加到数据库中
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {'code': 200, 'msg': 'success', 'data': {'post_id': db_post.post_id}}


@PostRouter.post("/getpost", summary="获取帖子")
def getpost(getpostinfo: GetPostBase, db: Session = Depends(get_db)):
    """
    获取帖子列表，这里需要一个几个参数
    categoryId: 贴子种类的id
    title: 帖子的标题 （一般模糊搜索）
    pageNum: 第几页
    pageSize: 每页返回的内容
    """

    print(getpostinfo)
    # total postList
    return {'code': 200, 'msg': 'success', 'getpostinfo': getpostinfo}
