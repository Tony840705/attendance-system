from sqlalchemy import Column, Integer, String, Date, DateTime
from backend.app.database import Base
from datetime import datetime, date


class ClockRecord(Base):
    __tablename__ = "clock_records"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, index=True, nullable=False)

    clock_type = Column(String, nullable=False)  # "in" or "out"
    clock_date = Column(Date, default=date.today, nullable=False)
    clock_time = Column(DateTime, default=datetime.utcnow, nullable=False)
