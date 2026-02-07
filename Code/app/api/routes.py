from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.schemas import SummarizeRequest, SummarizeResponse
from app.core.database import get_db
from app.controllers.summary_controller import SummaryController
from app.controllers.summary_controller import SummaryController
from app.controllers.history_controller import HistoryController
from app.controllers.health_controller import HealthController

router = APIRouter()

@router.get("/health")
async def check_health(db: Session = Depends(get_db)):
    controller = HealthController()
    return controller.check_health(db)

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_text(request: SummarizeRequest, db: Session = Depends(get_db)):
    controller = SummaryController()
    return controller.summarize(request, db)

@router.get("/history", response_model=list[dict])
async def get_history(limit: int = 50, db: Session = Depends(get_db)):
    controller = HistoryController()
    return controller.get_history(limit, db)
