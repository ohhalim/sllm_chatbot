from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import VECTOR
from sqlalchemy.sql import func
from src.database import Base

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    resume = Column(Text, nullable=False)
    job_posting = Column(Text, nullable=False)
    generated_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String, nullable=False)
    chunk_text = Column(Text, nullable=False)
    embedding = Column(VECTOR(1024), nullable=False) # 벡터 차원은 모델에 맞게 조정해야 합니다.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
