from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from backend.app.database import get_db
from backend.app.models.attendance import Attendance

router = APIRouter(
    prefix="/clock",
    tags=["Clock"]
)


@router.post("")
def clock(
    latitude: float,
    longitude: float,
    db: Session = Depends(get_db)
):
    user_id = 1  # 目前先寫死，之後再接登入系統

    today = date.today()

    today_records = (
        db.query(Attendance)
        .filter(
            Attendance.user_id == user_id,
            Attendance.timestamp >= today
        )
        .order_by(Attendance.timestamp.asc())
        .all()
    )

    if len(today_records) == 0:
        clock_type = "IN"
    elif len(today_records) == 1:
        clock_type = "OUT"
    else:
        raise HTTPException(status_code=400, detail="今日已完成上下班打卡")

    record = Attendance(
        user_id=user_id,
        clock_type=clock_type,
        latitude=latitude,
        longitude=longitude
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "clock_type": clock_type,
        "timestamp": record.timestamp,
        "latitude": latitude,
        "longitude": longitude
    }
