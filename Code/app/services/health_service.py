from sqlalchemy.orm import Session
from sqlalchemy import text

class HealthService:
    def check_db_status(self, db: Session) -> bool:
        try:
            db.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
