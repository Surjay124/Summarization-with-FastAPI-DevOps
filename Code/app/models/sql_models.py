from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from app.core.database import Base

class SummarizationLog(Base):
    __tablename__ = "summarization_logs"

    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(String, index=False)
    output_summary = Column(String, index=False)
    model_name = Column(String, index=True)
    response_time_seconds = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
