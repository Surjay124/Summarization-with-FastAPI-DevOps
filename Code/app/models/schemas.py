from pydantic import BaseModel, Field

class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to summarize")
    num_sentences: int = Field(3, ge=1, description="Number of sentences in the summary")

class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int
