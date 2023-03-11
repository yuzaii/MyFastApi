import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, load_only

from app.Utils.auth import auth_depend
from app.database import get_db
from app.models.CalendarModel import Calendar
from app.models.InformModel import Inform
from app.schemas.InfoCenterSchemas import CommitCalendar, CommitInform

InformApi = APIRouter(prefix='/inform', tags=['校园通知相关api'])


@InformApi.get('/getinform', summary='获取校园通知信息')
def get_inform(db: Session = Depends(get_db)):
    informlist = db.query(Inform).options(
        load_only(Inform.user_id, Inform.inform_id, Inform.inform_detail, Inform.inform_title, Inform.inform_date,
                  Inform.type)).order_by(Inform.inform_date.desc()).all()
    # print(123)
    return {'code': 200, 'msg': 'success', 'data': informlist}


@InformApi.get('/getinformbyid', summary='根据id获取校园通知信息')
def getinform_byid(id: int, db: Session = Depends(get_db)):
    # print(id)
    db_inforom = db.query(Inform).filter(Inform.inform_id == id).options(
        load_only(Inform.user_id, Inform.inform_id, Inform.inform_detail, Inform.inform_title, Inform.inform_date,
                  Inform.type)).first()

    return {'code': 200, 'msg': 'success', 'data': db_inforom}


@InformApi.post('/commitinform', summary='根据id获取校园通知信息')
def commit_inform(inform: CommitInform, db: Session = Depends(get_db), user=Depends(auth_depend)):
    print(inform)
    db_inform = Inform(user_id=user.user_id, inform_title=inform.title, inform_detail=inform.detail, inform_date=inform.date,
                       type=inform.type
                       , create_time=datetime.datetime.now(), state=0)
    db.add(db_inform)
    db.commit()
    return {'code': 200, 'msg': 'success'}
