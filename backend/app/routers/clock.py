from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date
from app.database import get_db
from app.models import Attendance
from pydantic import BaseModel
import sqlite3

router = APIRouter()

DB_PATH = "attendance.db"

class ClockRequest(BaseModel):
    employee_id: str
    type: str
    lat: float
    lng: float

@router.post("/api/clock")
def clock(req: ClockRequest):
    now = datetime.now()
    today = now.date()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if req.type == "in":
        cursor.execute("""
            INSERT INTO attendance (employee_id, date, clock_in_time)
            VALUES (?, ?, ?)
        """, (req.employee_id, today, now))
        msg = "上班打卡成功"

    elif req.type == "out":
        cursor.execute("""
            UPDATE attendance
            SET clock_out_time = ?
            WHERE employee_id = ? AND date = ?
        """, (now, req.employee_id, today))
        msg = "下班打卡成功"

    else:
        conn.close()
        return {"message": "未知打卡類型"}

    conn.commit()
    conn.close()

    return {"message": msg}