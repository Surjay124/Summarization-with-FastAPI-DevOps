from sqlalchemy.orm import Session
from app.models.sql_models import SummarizationLog
from app.core.config import settings

class LogService:
    def __init__(self, db: Session):
        self.db = db

    def create_log(self, input_text: str, output_summary: str, response_time: float) -> SummarizationLog:
        """
        Creates a new summarization log entry in the database.
        """
        try:
            log_entry = SummarizationLog(
                input_text=input_text,
                output_summary=output_summary,
                model_name=settings.MODEL_NAME,
                response_time_seconds=response_time
            )
            self.db.add(log_entry)
            self.db.commit()
            self.db.refresh(log_entry)
            return log_entry
        except Exception as e:
            self.db.rollback()
            # We log the error but re-raise or handle it depending on requirements.
            # In routes.py we were printing it. Here we might just re-raise.
            print(f"ERROR: Failed to save log to DB: {e}")
            raise e

    def get_history(self, limit: int = 50) -> list[SummarizationLog]:
        """
        Retrieves the most recent summarization logs.
        """
        return self.db.query(SummarizationLog).order_by(SummarizationLog.id.desc()).limit(limit).all()
