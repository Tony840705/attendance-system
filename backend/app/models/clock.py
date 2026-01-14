from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from backend.app.database import Base

class ClockRecord(Base):
    __tablename__ = "clock_records"

    id = Column(Integer, primary_key=True)
    employee_id = Column(String, index=True, nullable=False)
    work_date = Column(Date, index=True, nullable=False)
    clock_in_at = Column(DateTime)
    clock_out_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
