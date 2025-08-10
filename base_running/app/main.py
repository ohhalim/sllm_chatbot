from fastapi import FastAPI
from . import controller

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="Layered CRUD Backend",
    description="A FastAPI project with Controller, Service, and Repository layers designed for learning.",
    version="1.0.0",
)

# controller.py에 정의된 API 라우터를 애플리케이션에 포함시킵니다.
app.include_router(controller.router)

@app.get("/")
def read_root():
    """루트 경로, API 시작점을 알려줍니다."""
    return {"message": "Welcome to the Layered CRUD API. Go to /docs to see the API documentation."}
