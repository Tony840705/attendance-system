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

@router.post("/in") # 上班打卡
def clock_in(employee_id: str):
    db: Session = SessionLocal()
    today = date.today()

    record = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.date == today
    ).first()

    if record and record.clock_in_time:
        raise HTTPException(
            status_code=400,
            detail="今日已完成上班打卡，請勿重複打卡"
        )

    if not record:
        record = Attendance(
            employee_id=employee_id,
            date=today,
            clock_in_time=datetime.now()
        )
        db.add(record)
    else:
        record.clock_in_time = datetime.now()

    db.commit()

    return {"message": "上班打卡成功"}

@router.post("/out") #下班打卡
def clock_out(employee_id: str):
    db: Session = SessionLocal()
    today = date.today()

    record = db.query(Attendance).filter(
        Attendance.employee_id == employee_id,
        Attendance.date == today
    ).first()

    if not record or not record.clock_in_time:
        raise HTTPException(
            status_code=400,
            detail="尚未完成上班打卡，無法下班打卡"
        )

    if record.clock_out_time:
        raise HTTPException(
            status_code=400,
            detail="今日已完成下班打卡，請勿重複打卡"
        )

    record.clock_out_time = datetime.now()
    db.commit()

    return {"message": "下班打卡成功"}

@router.get("/records") #查詢打卡紀錄
def get_all_records():
    db: Session = SessionLocal()
    records = db.query(Attendance).order_by(
        Attendance.date.desc()
    ).all()

    return records

@router.get("/records/{employee_id}") #查詢指定員工紀錄
def get_employee_records(employee_id: str):
    db: Session = SessionLocal()
    records = db.query(Attendance).filter(
        Attendance.employee_id == employee_id
    ).order_by(Attendance.date.desc()).all()

    return records