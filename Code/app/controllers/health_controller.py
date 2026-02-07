from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.health_service import HealthService

class HealthController:
    def __init__(self):
        self.health_service = HealthService()

    def check_health(self, db: Session):
        db_status = self.health_service.check_db_status(db)
        if not db_status:
             raise HTTPException(status_code=503, detail="Database connection failed")
        
        return {"status": "ok", "database": "connected"}
