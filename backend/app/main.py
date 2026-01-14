from backend.app.database import Base, engine
from backend.app.routers import clock
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(clock.router)

@app.get("/")
def root():
    return {"status": "ok"}

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}