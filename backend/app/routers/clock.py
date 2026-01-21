from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date
from app.database import get_db
from app.models import Attendance
from pydantic import BaseModel

router = APIRouter(prefix="/api")

class ClockRequest(BaseModel):
    employee_id: str
    type: str
    lat: float
    lng: float

@router.post("/clock")
def clock(req: ClockRequest, db: Session = Depends(get_db)):
    today = date.today()

    record = db.query(Attendance).filter(
        Attendance.employee_id == req.employee_id,
        Attendance.date == today
    ).first()

    now = datetime.now()

    if not record:
        record = Attendance(
            employee_id=req.employee_id,
            date=today,
            clock_in_time=now
        )
        db.add(record)
        db.commit()
        return {"message": "上班打卡成功"}

    if record.clock_out_time is None:
        record.clock_out_time = now
        db.commit()
        return {"message": "下班打卡成功"}

    return {"message": "今日已完成打卡"}