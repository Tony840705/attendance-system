from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from backend.app.database import get_db
from backend.app import models, schemas

router = APIRouter(prefix="/api")

@router.post("/clock")
def clock(data: schemas.ClockRequest, db: Session = Depends(get_db)):
    now = datetime.now()

    record = models.Attendance(
        emp_id=data.emp_id,
        type=data.type,
        lat=data.lat,
        lng=data.lng,
        time=now
    )

    db.add(record)
    db.commit()

    if data.type == "in":
        return {"message": "上班打卡成功"}
    else:
        return {"message": "下班打卡成功"}
