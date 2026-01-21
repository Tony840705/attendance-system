from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import sqlite3

app = FastAPI()
DB = "attendance.db"
BASE_DIR = Path(__file__).resolve().parents[2]
STATIC_DIR = BASE_DIR / "static"

class ClockRequest(BaseModel):
    employee_id: str
    lat: float
    lng: float
    type: str  # in / out

def get_db():
    return sqlite3.connect(DB)

@app.post("/api/clock")
def clock(req: ClockRequest):
    conn = get_db()
    cur = conn.cursor()

    today = datetime.now().date().isoformat()
    now = datetime.now().strftime("%H:%M:%S")
    map_url = f"https://www.google.com/maps?q={req.lat},{req.lng}"

    if req.type == "in":
        cur.execute("""
        INSERT INTO attendance
        (employee_id, work_date, clock_in_time, clock_in_lat, clock_in_lng, clock_in_map)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (req.employee_id, today, now, req.lat, req.lng, map_url))

    else:
        cur.execute("""
        SELECT clock_in_time FROM attendance
        WHERE employee_id=? AND work_date=?
        """, (req.employee_id, today))
        clock_in = cur.fetchone()[0]

        t1 = datetime.strptime(clock_in, "%H:%M:%S")
        t2 = datetime.strptime(now, "%H:%M:%S")
        hours = round((t2 - t1).seconds / 3600, 2)

        cur.execute("""
        UPDATE attendance
        SET clock_out_time=?, clock_out_lat=?, clock_out_lng=?,
            clock_out_map=?, work_hours=?
        WHERE employee_id=? AND work_date=?
        """, (now, req.lat, req.lng, map_url, hours, req.employee_id, today))

    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.get("/api/attendance/{employee_id}")
def get_attendance(employee_id: str):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT work_date, clock_in_time, clock_out_time, work_hours
    FROM attendance
    WHERE employee_id=?
    ORDER BY work_date DESC
    """, (employee_id,))

    records = cur.fetchall()
    conn.close()

    attendance_list = []
    for row in records:
        attendance_list.append({
            "work_date": row[0],
            "clock_in_time": row[1],
            "clock_out_time": row[2],
            "work_hours": row[3]
        })

    return {"employee_id": employee_id, "attendance": attendance_list}

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")