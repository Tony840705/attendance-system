from pydantic import BaseModel


class ClockRequest(BaseModel):
    latitude: float
    longitude: float