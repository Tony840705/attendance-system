from backend.app.database import Base, engine
from backend.app.routers import clock
from fastapi import FastAPI

# 建立資料表
Base.metadata.create_all(bind=engine)

# 建立 FastAPI app
app = FastAPI()

# 包含 clock 路由
app.include_router(clock.router)

# 根路由
@app.get("/")
def root():
    return {"status": "ok"}