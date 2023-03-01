import datetime
import os
import time

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.Utils.Pagination import Pagination
from app.Utils.auth import auth_depend
from app.database import get_db
from app.models.PostCategoryModel import PostCategory
from app.models.PostModel import Post
from app.models.UserModel import User
from app.schemas.PostSchemas import PublisPostBase, GetPostBase

PostRouter = APIRouter(prefix='/post', tags=['论坛文章相关api'])


@PostRouter.get("/postcategory", summary="获取帖子种类学信息")
def getpostcategory(db: Session = Depends(get_db)):
    postcategorys = db.query(PostCategory).all()
    # print(postcategorys)
    return {'code': 200, 'msg': 'success', 'data': postcategorys}


@PostRouter.post("/postimg/upload", summary="上传帖子图片")
async def postimgupload(file: UploadFile = File(...), user=Depends(auth_depend)):
    print('postimgupload')
    user_id = user.user_id
    extension = os.path.splitext(file.filename)[1]
    new_filename = f"{user_id}-{int(time.time())}{extension}"
    file.filename = new_filename
    print('新的filename:', file.filename)
    # 将文件上传到upload文件夹中
    contents = await file.read()
    with open(f"./upload/img/postimg/{file.filename}", "wb") as f:
        f.write(contents)
    return {
        "errno": 0,
        "data": {
            "url": f"http://localhost:6060/img/postimg/{new_filename}",
            # "alt": "yyy",
            # "href": "zzz"
        }
    }


@PostRouter.post("/publishpost", summary="发布帖子")
def publishpost(post: PublisPostBase, db: Session = Depends(get_db), user=Depends(auth_depend)):
    # user_id = user.user_id
    print(post)
    # 构造帖子对象
    db_post = Post(user_id=user.user_id, title=post.title, detail=post.detail,
                   images=post.images, comment_num=0, view_num=0, best_post=0,
                   category_id=post.category_id, create_time=datetime.datetime.now(),
                   collect_num=0, post_status=0)
    print(db_post)
    # 将贴子添加到数据库中
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return {'code': 200, 'msg': 'success', 'data': {'post_id': db_post.post_id}}


@PostRouter.post("/getpost", summary="获取帖子信息")
def getpost(getpostinfo: GetPostBase, db: Session = Depends(get_db)):
    """
    获取帖子列表，这里需要一个几个参数
    categoryId: 贴子种类的id
    pageNum: 第几页
    pageSize: 每页的大小
    """

    # 有title无有category_id参数 也就是title是所有返回的搜索
    # 如果有title就带title查询
    # if getpostinfo.title:
    #     print('有title参数')
    #     postlist=db.query(Post).filter_by()
    # else:
    #     print('无title参数')

    # 如果参数有category_id的话就带category_id查询
    print('getpostinfo:', getpostinfo)
    if getpostinfo.category_id:
        print('有category_id参数')
        post_query = db.query(Post, User.username).select_from(Post).join(User).filter(
            Post.category_id == getpostinfo.category_id).order_by(Post.create_time.desc())
        postdata, total = Pagination(post_query, getpostinfo.pageNum, getpostinfo.pageSize).paginate()
        postinfolist = [p._asdict() for p in postdata]

        # post_query = db.query(Post).filter_by(category_id=getpostinfo.category_id).join(User,
        #                                                                                 User.user_id == Post.user_id)
        #
        # postlist, total = Pagination(post_query, getpostinfo.pageNum, getpostinfo.pageSize).paginate()
        print(f'一共{total}条帖子数据')
        # print(postlist)
        return {'code': 200, 'msg': 'success', 'data': {"total": total, 'postinfolist': postinfolist}}
    else:
        print('没有category_id参数')
        post_query = db.query(Post, User.username).select_from(Post).join(User).order_by(Post.create_time.desc())
        postdata, total = Pagination(post_query, getpostinfo.pageNum, getpostinfo.pageSize).paginate()
        postinfolist = [p._asdict() for p in postdata]
        print(f'一共{total}条帖子数据')
        # print(postlist)
        return {'code': 200, 'msg': 'success', 'data': {"total": total, 'postinfolist': postinfolist}}


@PostRouter.get("/getbypostid", summary="根据postid获取帖子信息")
def getpostbyid(id: int, db: Session = Depends(get_db)):
    post_query = db.query(Post, User.username, PostCategory.category_name).select_from(Post).filter_by(post_id=id).join(
        User).join(
        PostCategory).first()
    postinfo = post_query._asdict()
    print(postinfo)
    return {'code': 200, 'msg': 'success', 'data': {'postinfo': postinfo}}
