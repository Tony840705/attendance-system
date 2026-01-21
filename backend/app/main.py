from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3
from datetime import datetime, date

app = FastAPI()

# ===== Static =====
app.mount("/static", StaticFiles(directory="static"), name="static")

# ===== DB =====
DB_PATH = "attendance.db"

def get_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT NOT NULL,
        date TEXT NOT NULL,
        type TEXT NOT NULL,
        time TEXT NOT NULL,
        lat REAL,
        lng REAL,
        UNIQUE(employee_id, date, type)
    )
    """)
    conn.commit()
    conn.close()

@app.on_event("startup")
def startup():
    init_db()
    print("✅ Attendance system started")

# ===== Schema =====
class ClockReq(BaseModel):
    employee_id: str
    type: str   # in / out
    lat: float
    lng: float

# ===== API =====
@app.post("/api/clock")
def clock(req: ClockReq):
    today = date.today().isoformat()
    now = datetime.now().strftime("%H:%M:%S")

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
        INSERT INTO attendance (employee_id, date, type, time, lat, lng)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            req.employee_id,
            today,
            req.type,
            now,
            req.lat,
            req.lng
        ))
        conn.commit()

    except sqlite3.IntegrityError:
        conn.close()
        return {
            "success": False,
            "message": f"❌ 今日已完成「{ '上班' if req.type == 'in' else '下班' }」打卡，請勿重複打卡"
        }

    conn.close()
    return {
        "success": True,
        "message": f"✅ {req.employee_id} { '上班' if req.type == 'in' else '下班' } 打卡成功 ({now})"
    }

# ===== Health =====
@app.get("/health")
def health():
    return {"ok": True}
@app.get("/api/my-today/{employee_id}")
def my_today(employee_id: str):
    today = date.today().isoformat()
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT type, time FROM attendance
    WHERE employee_id=? AND date=?
    """, (employee_id, today))

    rows = cur.fetchall()
    conn.close()

    return {
        "employee_id": employee_id,
        "date": today,
        "records": [
            {"type": r[0], "time": r[1]} for r in rows
        ]
    }
@app.get("/api/admin/today")
def admin_today():
    today = date.today().isoformat()
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT employee_id, type, time, lat, lng
    FROM attendance
    WHERE date=?
    ORDER BY employee_id
    """, (today,))

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "employee_id": r[0],
            "type": r[1],
            "time": r[2],
            "lat": r[3],
            "lng": r[4]
        } for r in rows
    ]