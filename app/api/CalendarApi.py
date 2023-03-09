import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.Utils.auth import auth_depend
from app.database import get_db
from app.models.CalendarModel import Calendar
from app.schemas.InfoCenterSchemas import CommitCalendar

CalendarApi = APIRouter(prefix='/calendar', tags=['校园日历相关api'])


@CalendarApi.get('/getcalendarinfo', summary='获取所有校园日历日期信息')
def get_calendarinfo(db: Session = Depends(get_db)):
    db_caledarinfo = db.query(Calendar).all()
    print(db_caledarinfo)
    caledar_dict = {}
    # print(caledar_dict.keys())
    for caledar in db_caledarinfo:
        # 判断是否在caledar_dict中
        print('caledar_dict.keys()', caledar_dict.keys())
        if caledar.date in caledar_dict.keys():
            print('in', caledar)
            caledar_dict[caledar.date].append(caledar.date_name)
        else:
            print('no', caledar)
            caledar_dict[caledar.date] = [caledar.date_name]
    return {'data': caledar_dict, 'code': 200, 'msg': 'success'}


@CalendarApi.post('/commitcalendar', summary='提交校园日历日期信息')
def commit_calendar(calendar: CommitCalendar, db: Session = Depends(get_db), user=Depends(auth_depend)):
    print(user)
    print(calendar)
    db_calendar = Calendar(date_name=calendar.name, date=calendar.date, user_id=user.user_id,
                           create_time=datetime.datetime.now())
    db.add(db_calendar)
    db.commit()
    return {'code': 200, 'msg': 'success'}
