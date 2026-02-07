from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.schemas import SummarizeRequest, SummarizeResponse
from app.services.ai_provider import ai_provider
from app.services.log_service import LogService
import time

class SummaryController:
    def summarize(self, request: SummarizeRequest, db: Session) -> SummarizeResponse:
        start_time = time.time()
        
        # 1. AI Summarization (Validation happens inside provider)
        try:
            summary = ai_provider.summarize(request.text, request.num_sentences)
        except ValueError as ve:
            # Map domain/service errors to HTTP 400
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI Provider failed: {str(e)}")

        duration = time.time() - start_time
        
        # 2. Persist Log (Fire and forget style, or robust)
        log_service = LogService(db)
        try:
            log_service.create_log(
                input_text=request.text,
                output_summary=summary,
                response_time=duration
            )
        except Exception:
            # Log failure to save shouldn't block response, mimicking previous behavior
            # In a real app we might log this to a file or monitoring system
            pass

        return SummarizeResponse(
            summary=summary,
            original_length=len(request.text),
            summary_length=len(summary)
        )
