from fastapi import FastAPI
from src.database import engine, Base

# 데이터베이스 테이블 생성
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_tables()

@app.get("/")
async def root():
    return {"message": "Hello World, database tables are ready!"}
