import datetime

from fastapi import APIRouter, Depends
from flask_sqlalchemy.session import Session

from app.Utils.auth import auth_depend
from app.database import get_db
from app.models.UrlinfoModel import Urlinfo
from app.schemas.UrlSchemas import CommitUrlinfo

UrlRouter = APIRouter(prefix='/urlnav', tags=['链接导航相关api'])


@UrlRouter.get('/geturlinfo', summary='获取链接信息')
def get_urlinfo(db: Session = Depends(get_db)):
    url_list = db.query(Urlinfo).all()
    return {'code': 200, 'msg': 'success', 'data': url_list}


@UrlRouter.post('/commiturl', summary="提交链接信息")
def commiturl(urlinfo: CommitUrlinfo, db: Session = Depends(get_db), user=Depends(auth_depend)):
    print(urlinfo)
    print(user)
    db_urlinfo = Urlinfo(url_name=urlinfo.name, url=urlinfo.url, url_description=urlinfo.description,
                         type=urlinfo.type, user_id=user.user_id, create_time=datetime.datetime.now(),
                         tags=str(urlinfo.tags))
    db.add(db_urlinfo)
    db.commit()
    return {'code': 200, 'msg': 'success'}
