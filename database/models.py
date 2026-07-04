from pydantic import BaseModel, Field
from typing import Optional, List

class SetLogRequest(BaseModel):
    exercise_key: str
    set_number: int
    reps_counted: int
    weight_kg: float = 0.0
    rpe: int = Field(..., ge=1, le=10)
    avg_form_score: float
    pain_flag: bool = False
    pain_location: Optional[str] = ""

class SessionEndRequest(BaseModel):
    notes: Optional[str] = ""
