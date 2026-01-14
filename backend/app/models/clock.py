from fastapi import APIRouter, HTTPException
from sqlalchemy import Column, Integer, String, Date, DateTime
from datetime import datetime, date

from backend.app.database import Base
from backend.app.models.attendance import Attendance

class ClockRecord(Base):
    __tablename__ = "clock_records"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, index=True, nullable=False)

    clock_type = Column(String, nullable=False)  # in / out
    clock_time = Column(DateTime, default=datetime.utcnow)
    clock_date = Column(Date, default=date.today)