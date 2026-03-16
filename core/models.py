from pydantic import BaseModel
from typing import Optional, List

class Job(BaseModel):
    id: str
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str
    distance_km: Optional[float] = None
    visa_risk: Optional[str] = None
    fit_score: Optional[int] = None

class ResumeProfile(BaseModel):
    name: str
    file_path: str
    tags: List[str]

class ReviewDecision(BaseModel):
    job_id: str
    action: str  # apply / skip / edit_resume / edit_answers