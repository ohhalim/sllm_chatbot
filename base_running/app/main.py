from fastapi import FastAPI
from . import controller, midi_controller

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="Layered CRUD and MIDI RAG Backend",
    description="A FastAPI project with Controller, Service, and Repository layers, including MIDI generation.",
    version="1.1.0",
)

# 컨트롤러 라우터 포함
app.include_router(controller.router)
app.include_router(midi_controller.router)

@app.get("/")
def read_root():
    """루트 경로, API 시작점을 알려줍니다."""
    return {"message": "Welcome to the API. Go to /docs to see the API documentation."}
