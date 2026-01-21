# 打卡紀錄 Model
from sqlalchemy import Column, Integer, DateTime, Float, String
from backend.app.database import Base
from datetime import datetime

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(String, index=True)
    date = Column(String, index=True)

    clock_in_time = Column(DateTime, nullable=True)
    clock_out_time = Column(DateTime, nullable=True)

    clock_in_lat = Column(Float, nullable=True)
    clock_in_lng = Column(Float, nullable=True)

    clock_out_lat = Column(Float, nullable=True)
    clock_out_lng = Column(Float, nullable=True)

    work_hours = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)