from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services.log_service import LogService

class HistoryController:
    def get_history(self, limit: int, db: Session) -> list[dict]:
        try:
            log_service = LogService(db)
            logs = log_service.get_history(limit)
            
            return [
                {
                    "id": log.id,
                    "input_text": log.input_text,
                    "output_summary": log.output_summary,
                    "model_name": log.model_name,
                    "created_at": log.created_at,
                    "response_time_seconds": log.response_time_seconds
                }
                for log in logs
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")
