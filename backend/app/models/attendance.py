# 打卡紀錄 Model
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from backend.app.database import Base


class Attendance(Base):
    __tablename__ = "Attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, index=True)      # 員工編號
    date = Column(Date, index=True)               # 打卡日期
    clock_in_time = Column(DateTime, nullable=True)
    clock_out_time = Column(DateTime, nullable=True)
