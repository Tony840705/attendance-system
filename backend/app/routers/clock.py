from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from datetime import datetime

from backend.app.database import get_db
from backend.app.models.attendance import Attendance
from backend.app.schemas.clock import ClockRequest

router = APIRouter(
    prefix="/clock",
    tags=["Clock"]
)


@router.post("/")
def clock(
    user_id: str,
    lat: float,
    lng: float,
    action: str,   # "in" or "out"
    db: Session = Depends(get_db)
):
    today = datetime.now().strftime("%Y-%m-%d")

    record = db.query(Attendance).filter(
        Attendance.user_id == user_id,
        Attendance.date == today
    ).first()

    if action == "in":
        if record and record.clock_in_time:
            raise HTTPException(status_code=400, detail="已打過上班卡")

        if not record:
            record = Attendance(user_id=user_id, date=today)
            db.add(record)

        record.clock_in_time = datetime.now()
        record.clock_in_lat = lat
        record.clock_in_lng = lng

    elif action == "out":
        if not record or not record.clock_in_time:
            raise HTTPException(status_code=400, detail="尚未上班打卡")

        if record.clock_out_time:
            raise HTTPException(status_code=400, detail="已打過下班卡")

        record.clock_out_time = datetime.now()
        record.clock_out_lat = lat
        record.clock_out_lng = lng

        delta = record.clock_out_time - record.clock_in_time
        record.work_hours = round(delta.total_seconds() / 3600, 2)

    else:
        raise HTTPException(status_code=400, detail="action 錯誤")

    db.commit()

    return {
        "message": "打卡成功",
        "work_hours": record.work_hours
    }