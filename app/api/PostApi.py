import datetime
import os
import time

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session, subqueryload, load_only

from app.Utils.Pagination import Pagination
from app.Utils.auth import auth_depend
from app.database import get_db
from app.models.PostCategoryModel import PostCategory
from app.models.PostModel import Post
from app.models.UserModel import User
from app.schemas.PostSchemas import PublisPostBase, GetPostBase, SearchBase

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
    print('getpostinfo:', getpostinfo)
    # 有title无有category_id参数 也就是title是所有返回的搜索
    # 如果参数有category_id的话就带category_id查询
    if getpostinfo.category_id:
        print('有category_id参数')
        # post_query = db.query(Post, User.username).select_from(Post).join(User).filter(
        #     Post.category_id == getpostinfo.category_id).order_by(Post.create_time.desc())
        post_query = db.query(Post).filter_by(category_id=getpostinfo.category_id).options(
            subqueryload(Post.user).load_only(User.username)).order_by(Post.create_time.desc())

        postlist, total = Pagination(post_query, getpostinfo.pageNum, getpostinfo.pageSize).paginate()
        # postinfolist = [p._asdict() for p in postdata]

        # post_query = db.query(Post).filter_by(category_id=getpostinfo.category_id).join(User,
        #                                                                                 User.user_id == Post.user_id)
        #
        # postlist, total = Pagination(post_query, getpostinfo.pageNum, getpostinfo.pageSize).paginate()
        print(f'一共{total}条帖子数据')
        # print(postlist)
        return {'code': 200, 'msg': 'success', 'data': {"total": total, 'postlist': postlist}}
    else:
        # 如果没有就查询全部
        print('没有category_id参数')
        post_query = db.query(Post).options(subqueryload(Post.user).load_only(User.username)).order_by(
            Post.create_time.desc())
        # post_query = db.query(Post, User.username).select_from(Post).join(User).order_by(Post.create_time.desc())
        postlist, total = Pagination(post_query, getpostinfo.pageNum, getpostinfo.pageSize).paginate()
        # postinfolist = [p._asdict() for p in postdata]
        print(f'一共{total}条帖子数据')
        # print(postlist)
        return {'code': 200, 'msg': 'success', 'data': {"total": total, 'postlist': postlist}}
    # 如果啥都没有就是全部


@PostRouter.get("/gethotpost", summary="获取热门帖子信息")
def gethotpost(db: Session = Depends(get_db)):
    # users = db.query(User).options(load_only(User.username)).all()
    # print(users)
    # for user in users:
    #     print(user)
    hotposts = db.query(Post).options(load_only(Post.title, Post.create_time)).order_by(Post.view_num.desc()).limit(
        10).all()
    # print(hotposts)
    # print(len(hotposts))
    return {'code': 200, 'msg': 'success', 'data': {'hotposts': hotposts}}


@PostRouter.get("/getbypostid", summary="根据postid获取帖子信息")
def getpostbyid(post_id: int, db: Session = Depends(get_db)):
    # post_query = db.query(Post, User.username, PostCategory.category_name).select_from(Post).filter_by(post_id=id).join(
    #     User).join(
    #     PostCategory).first()
    # postinfo = post_query._asdict()
    postinfo = db.query(Post).filter_by(post_id=post_id).options(
        subqueryload(Post.user).load_only(User.username)).options(
        subqueryload(Post.post_category).load_only(PostCategory.category_name)).first()
    # 增加文章浏览量
    postinfo.view_num += 1
    db.commit()
    db.refresh(postinfo)
    # print(postinfo)
    # post_query=db.query(Post).options(subqueryload(Post))
    # print(post_query)
    return {'code': 200, 'msg': 'success', 'data': {'postinfo': postinfo}}


@PostRouter.post("/searchpost", summary="搜索帖子信息")
def searchpost(searchquery: SearchBase, db: Session = Depends(get_db)):
    print('searchquery')
    post_query = db.query(Post).filter(Post.title.like(f'%{searchquery.searchTitle}%')).options(
        subqueryload(Post.user).load_only(User.username)).order_by(
        Post.create_time.desc())
    postlist, total = Pagination(post_query, searchquery.pageNum, searchquery.pageSize).paginate()

    return {'code': 200, 'msg': 'success', 'data': {"total": total, 'postlist': postlist}}
