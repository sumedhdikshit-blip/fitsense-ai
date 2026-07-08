from pydantic import BaseModel, Field
from typing import Optional

class SetLogRequest(BaseModel):
    session_id: Optional[int] = None
    exercise_key: str
    set_number: int
    reps_counted: int
    weight_kg: float = Field(..., ge=0)
    weight_unit: str = Field("kg", pattern="^(kg|lbs)$")
    weight_mode: Optional[str] = "total"
    rpe: int = Field(..., ge=1, le=10)
    avg_form_score: Optional[float] = 0.0   # 0.0 for manual entries (no camera data)
    pain_flag: bool = False
    pain_location: Optional[str] = Field("", max_length=100)
    duration_seconds: float = 0.0

class SessionEndRequest(BaseModel):
    session_id: int
    notes: Optional[str] = Field("", max_length=500)

class ProfileRequest(BaseModel):
    name: str
    age: int = Field(..., ge=1, le=120)
    weight_kg: float = Field(..., ge=10, le=500)
    height_cm: float = Field(..., ge=50, le=300)
    sex: str = Field("unspecified", pattern="^(male|female|unspecified)$")
    fitness_goal: Optional[str] = ""
    gender: Optional[str] = Field(None, pattern="^(male|female|other)$")
    diet_quality: Optional[str] = Field(None, pattern="^(poor|average|good|excellent)$")
    stress_level: Optional[int] = Field(None, ge=1, le=10)
    sleep_hours: Optional[float] = Field(None, ge=0, le=24)
    smoker: Optional[str] = Field(None, pattern="^(yes|no)$")
    exercise_freq: Optional[str] = Field(None, pattern="^(none|1-2 times/week|3-5 times/week|daily)$")
    alcohol_consumption: Optional[str] = Field(None, pattern="^(none|low|moderate|high)$")

class WeightLogRequest(BaseModel):
    weight_kg: float = Field(..., ge=10, le=500)
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD

class CardioLogRequest(BaseModel):
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD
    activity_name: str = Field(..., max_length=100)
    duration_mins: float = Field(0.0, ge=0)
    calories_burned: float = Field(..., ge=0)
    entry_method: str = Field(..., pattern="^(duration|direct_calories)$")

class NutritionLogRequest(BaseModel):
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD
    calories_consumed: float = Field(..., ge=0)
    protein_g: float = Field(0.0, ge=0)
    carbs_g: float = Field(0.0, ge=0)
    fat_g: float = Field(0.0, ge=0)
    saturated_fat_g: float = Field(0.0, ge=0)
    fiber_g: float = Field(0.0, ge=0)
    sodium_mg: float = Field(0.0, ge=0)
    sugar_g: float = Field(0.0, ge=0)
    calcium_mg: float = Field(0.0, ge=0)
    iron_mg: float = Field(0.0, ge=0)
    vitamin_c_mg: float = Field(0.0, ge=0)

class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=1, max_length=100)

class UserLoginRequest(BaseModel):
    username: str
    password: str

class RiskEstimateRequest(BaseModel):
    age: Optional[int] = Field(None, ge=1, le=120)
    gender: Optional[str] = Field(None, pattern="^(male|female|other)$")
    height_cm: Optional[float] = Field(None, ge=50, le=300)
    weight_kg: Optional[float] = Field(None, ge=10, le=500)
    bmi: Optional[float] = Field(None, ge=0)
    smoker: Optional[str] = Field(None, pattern="^(yes|no)$")
    diet_quality: Optional[str] = Field(None, pattern="^(poor|average|good|excellent)$")
    stress_level: Optional[int] = Field(None, ge=1, le=10)
    sleep_hours: Optional[float] = Field(None, ge=0, le=24)
    exercise_freq: Optional[str] = Field(None, pattern="^(none|1-2 times/week|3-5 times/week|daily)$")
    alcohol_consumption: Optional[str] = Field(None, pattern="^(none|low|moderate|high)$")

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)
    confirm_new_password: str

class WeightGoalRequest(BaseModel):
    goal_type: str = Field(..., pattern="^(lose|gain|maintain)$")
    target_weight_kg: float = Field(..., ge=10, le=500)
    starting_weight_kg: float = Field(..., ge=10, le=500)
    target_date: Optional[str] = None
    pace: Optional[str] = Field(None, pattern="^(mild|normal|aggressive|)$")
    muscle_focus: Optional[str] = Field(None, pattern="^(preserve|lean|bulk|)$")
    maintenance_focus: Optional[str] = Field(None, pattern="^(stay_fit|build_muscle|)$")


class BarcodeScanRequest(BaseModel):
    image_base64: str



