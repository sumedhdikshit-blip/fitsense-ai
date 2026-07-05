from pydantic import BaseModel, Field
from typing import Optional

class SetLogRequest(BaseModel):
    session_id: Optional[int] = None
    exercise_key: str
    set_number: int
    reps_counted: int
    weight_kg: float = 0.0
    weight_mode: Optional[str] = "total"
    rpe: int = Field(..., ge=1, le=10)
    avg_form_score: float
    pain_flag: bool = False
    pain_location: Optional[str] = ""
    duration_seconds: float = 0.0

class SessionEndRequest(BaseModel):
    session_id: int
    notes: Optional[str] = ""

class ProfileRequest(BaseModel):
    name: str
    age: int = Field(..., ge=1, le=120)
    weight_kg: float = Field(..., ge=10, le=500)
    height_cm: float = Field(..., ge=50, le=300)
    sex: str = Field("unspecified", pattern="^(male|female|unspecified)$")
    fitness_goal: Optional[str] = ""

class WeightLogRequest(BaseModel):
    weight_kg: float = Field(..., ge=10, le=500)
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD

class CardioLogRequest(BaseModel):
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD
    activity_name: str
    duration_mins: float = Field(0.0, ge=0)
    calories_burned: float = Field(..., ge=0)
    entry_method: str = Field(..., pattern="^(duration|direct_calories)$")

class NutritionLogRequest(BaseModel):
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD
    calories_consumed: float = Field(..., ge=0)
    protein_g: float = Field(0.0, ge=0)
    carbs_g: float = Field(0.0, ge=0)
    fat_g: float = Field(0.0, ge=0)
