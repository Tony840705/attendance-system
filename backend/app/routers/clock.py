from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from backend.app.database import get_db
from backend.app.models.clock import ClockRecord

router = APIRouter(prefix="/clock", tags=["Clock"])


@router.post("/in")
def clock_in(employee_id: str, db: Session = Depends(get_db)):
    today = date.today()

    existing = db.query(ClockRecord).filter(
        ClockRecord.employee_id == employee_id,
        ClockRecord.clock_date == today,
        ClockRecord.clock_type == "in"
    ).first()

    if existing:
        return {"message": "今日已打卡（上班）"}

    record = ClockRecord(
        employee_id=employee_id,
        clock_type="in"
    )

    db.add(record)
    db.commit()

    return {"message": "上班打卡成功"}
