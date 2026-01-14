# 打卡紀錄 Model
from sqlalchemy import Column, Integer, Float, DateTime, String
from datetime import datetime

from backend.app.database import Base


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)

    clock_type = Column(String(10))  # IN / OUT
    latitude = Column(Float)
    longitude = Column(Float)

    timestamp = Column(DateTime, default=datetime.utcnow)
