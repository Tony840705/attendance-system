from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ClockReq(BaseModel):
    employee_id: str
    type: str
    lat: float
    lng: float

@app.post("/api/clock")
def clock(req: ClockReq):
    return {
        "success": True,
        "message": f"{req.employee_id} {req.type} 打卡成功"
    }
