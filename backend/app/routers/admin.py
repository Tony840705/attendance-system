# 公司查看紀錄
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.attendance import Attendance

router = APIRouter(prefix="/api/admin")

@router.get("/Attendance")
def list_Attendance(db: Session = Depends(get_db)):
    records = db.query(Attendance).all()
    return records

import csv
from fastapi.responses import StreamingResponse

@router.get("/Attendance/export")
def export_Attendance(db: Session = Depends(get_db)):
    def generate():
        yield "date,name,check_in,check_out,distance\n"
        for r in db.query(Attendance).all():
            yield f"{r.date},{r.user.name},{r.check_in},{r.check_out},{r.distance_m}\n"

    return StreamingResponse(
        generate(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=Attendance.csv"}
    )

