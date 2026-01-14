from fastapi import APIRouter, HTTPException
from datetime import datetime, date
from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models.clock import ClockRecord

router = APIRouter(prefix="/clock", tags=["Clock"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/in")
def clock_in(employee_id: str):
    db: Session = next(get_db())
    today = date.today()

    record = db.query(ClockRecord).filter(
        ClockRecord.employee_id == employee_id,
        ClockRecord.work_date == today
    ).first()

    if record and record.clock_in_at:
        raise HTTPException(400, "Already clocked in today")

    if not record:
        record = ClockRecord(
            employee_id=employee_id,
            work_date=today,
            clock_in_at=datetime.now()
        )
        db.add(record)
    else:
        record.clock_in_at = datetime.now()

    db.commit()
    return {"message": "clock in success"}
