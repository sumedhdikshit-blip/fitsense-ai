import base64
import cv2
import numpy as np
import asyncio
import uvicorn
from concurrent.futures import ThreadPoolExecutor

pose_executor = ThreadPoolExecutor(max_workers=4)
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse, JSONResponse
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from config.exercise_library import EXERCISE_LIBRARY
from database import db, models
from pose.detector import PoseDetector, calculate_angle
from pose.counter import RepCounter

# Lifespan manager for FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database
    db.init_db()
    yield
    # Shutdown executor
    pose_executor.shutdown(wait=True)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="FitSense AI Core Engine", lifespan=lifespan)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please try again later."}
    )

session_secret = os.environ.get("SESSION_SECRET")
if not session_secret:
    raise RuntimeError("SESSION_SECRET environment variable is required")
app.add_middleware(SessionMiddleware, secret_key=session_secret)

def get_current_user_id(request: Request) -> int:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    return user_id


def decode_base64_frame(base64_str: str) -> np.ndarray:
    try:
        if "," in base64_str:
            base64_str = base64_str.split(",")[1]
        img_bytes = base64.b64decode(base64_str)
        np_arr = np.frombuffer(img_bytes, dtype=np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return frame
    except Exception as e:
        print(f"Error decoding base64 frame: {e}")
        return None

def encode_frame_to_base64(frame: np.ndarray) -> str:
    try:
        _, buffer = cv2.imencode('.jpg', frame)
        base64_str = base64.b64encode(buffer).decode('utf-8')
        return base64_str
    except Exception as e:
        print(f"Error encoding frame: {e}")
        return ""

def calculate_bmr(weight: float, height: float, age: int, sex: str) -> float:
    """
    Calculates Basal Metabolic Rate using Mifflin-St Jeor equation.
    """
    if sex == "male":
        return 10.0 * weight + 6.25 * height - 5.0 * age + 5.0
    elif sex == "female":
        return 10.0 * weight + 6.25 * height - 5.0 * age - 161.0
    else:
        # Unspecified: Average of male and female BMR
        male_bmr = 10.0 * weight + 6.25 * height - 5.0 * age + 5.0
        female_bmr = 10.0 * weight + 6.25 * height - 5.0 * age - 161.0
        return (male_bmr + female_bmr) / 2.0

def get_nutrition_breakdown_internal(user_id, date_str, profile):
    nutrition = db.get_nutrition_data(user_id, date_str)
    if not nutrition:
        nutrition = {
            "calories_consumed": 0.0,
            "protein_g": 0.0,
            "carbs_g": 0.0,
            "fat_g": 0.0
        }
        
    if profile and profile.get("weight_kg") and profile.get("height_cm") and profile.get("age"):
        bmr = calculate_bmr(profile["weight_kg"], profile["height_cm"], profile["age"], profile.get("sex", "unspecified"))
    else:
        bmr = 0.0
        
    conn = db.get_connection()
    try:
        cursor = conn.cursor()
        
        # Sum webcam sessions calories on this day
        cursor.execute("SELECT SUM(total_calories_burned) as cal FROM sessions WHERE user_id = ? AND date = ?", (user_id, date_str))
        webcam_row = cursor.fetchone()
        webcam_cals = webcam_row["cal"] if (webcam_row and webcam_row["cal"]) else 0.0
        
        # Sum cardio logs calories on this day
        cursor.execute("SELECT SUM(calories_burned) as cal FROM cardio_logs WHERE user_id = ? AND date = ?", (user_id, date_str))
        cardio_row = cursor.fetchone()
        cardio_cals = cardio_row["cal"] if (cardio_row and cardio_row["cal"]) else 0.0
    finally:
        conn.close()
        
    exercise_burn = webcam_cals + cardio_cals
    consumed = nutrition.get("calories_consumed") or 0.0
    tef = consumed * 0.10
    
    net = consumed - (exercise_burn + bmr + tef)
    
    return {
        "date": date_str,
        "calories_consumed": consumed,
        "protein_g": nutrition.get("protein_g") or 0.0,
        "carbs_g": nutrition.get("carbs_g") or 0.0,
        "fat_g": nutrition.get("fat_g") or 0.0,
        "calories_burned_exercise": exercise_burn,
        "calories_burned_bmr": bmr,
        "tef_calories": tef,
        "net_calories": net
    }

# ==================== ENDPOINTS ====================

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/ai/test-connection")
def test_ai_connection(user_id: int = Depends(get_current_user_id)):
    from ai.coach_client import get_groq_client
    try:
        client = get_groq_client()
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say hello in 5 words",
                }
            ],
            model="llama3-8b-8192",
        )
        reply = chat_completion.choices[0].message.content.strip()
        return {"status": "success", "reply": reply}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Groq API connection failed: {str(e)}")

def calculate_fitness_score_internal(user_id: int):
    """
    Calculates the user's current Fitness Score on a scale of 1.00 to 10.00.
    
    Composition:
    - 82% weight: Lifestyle/health sub-score (weighted average of normalized 0-10 sub-scores)
      - Age component (25% weight): Normalized based on age ranges.
      - BMI component (25% weight): Derived from weight and height, normalized based on clinical healthy range.
      - Stress component (25% weight): Normalized from stress_level (1-10), clamped gently to avoid harsh penalties.
      - Sleep component (25% weight): Normalized from sleep_hours (0-24), clamped gently to avoid harsh penalties.
    - 18% weight: Actual app activity sub-score (weighted average of normalized 0-10 activity sub-scores)
      - Consistency (35% weight): Count of sessions in the last 7 days.
      - Average Form Score (35% weight): Average form score of camera-tracked sets in the last 7 days.
      - Calorie Balance (15% weight): Daily net calories deviation from target based on user fitness goal.
      - PR Progress (15% weight): Count of personal records set in the last 7 days.
    """
    import datetime
    
    profile = db.get_profile(user_id)
    if not profile:
        profile = {
            "age": 28,
            "weight_kg": 75.0,
            "height_cm": 180.0,
            "sex": "unspecified",
            "stress_level": None,
            "sleep_hours": None,
            "fitness_goal": ""
        }
        
    missing_inputs = []
    
    # --- Lifestyle Score (82% weight) ---
    age = profile.get("age")
    if age is None:
        age = 28
    
    if 18 <= age <= 40:
        age_score = 10.0
    elif age < 18:
        age_score = max(2.0, (age / 18.0) * 10.0)
    else:
        age_score = max(2.0, 10.0 - (age - 40) * 0.15)
        
    weight = profile.get("weight_kg")
    height = profile.get("height_cm")
    if weight is None or weight <= 0:
        weight = 75.0
    if height is None or height <= 0:
        height = 180.0
        
    bmi = weight / ((height / 100.0) ** 2)
    if 18.5 <= bmi <= 24.9:
        bmi_score = 10.0
    elif bmi < 18.5:
        bmi_score = max(2.0, 10.0 - (18.5 - bmi) * 1.5)
    else:
        bmi_score = max(2.0, 10.0 - (bmi - 24.9) * 0.8)
        
    stress = profile.get("stress_level")
    stress_score = None
    if stress is None:
        missing_inputs.append("stress_level")
    else:
        stress_score = max(4.0, 11.0 - stress)
        
    sleep = profile.get("sleep_hours")
    sleep_score = None
    if sleep is None:
        missing_inputs.append("sleep_hours")
    else:
        if 7.0 <= sleep <= 9.0:
            sleep_score = 10.0
        elif sleep < 7.0:
            sleep_score = max(4.0, 10.0 - (7.0 - sleep) * 1.5)
        else:
            sleep_score = max(5.0, 10.0 - (sleep - 9.0) * 1.0)
            
    lifestyle_components = {
        "age": round(age_score, 2),
        "bmi": round(bmi_score, 2)
    }
    avail_lifestyle = [age_score, bmi_score]
    if stress_score is not None:
        lifestyle_components["stress_level"] = round(stress_score, 2)
        avail_lifestyle.append(stress_score)
    if sleep_score is not None:
        lifestyle_components["sleep_hours"] = round(sleep_score, 2)
        avail_lifestyle.append(sleep_score)
        
    lifestyle_avg = sum(avail_lifestyle) / len(avail_lifestyle)
    
    # --- Activity Score (18% weight) ---
    today = datetime.date.today()
    seven_days_ago_date = today - datetime.timedelta(days=7)
    seven_days_ago_str = seven_days_ago_date.strftime("%Y-%m-%d")
    
    conn = db.get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as cnt FROM sessions 
            WHERE user_id = ? AND date >= ?
        """, (user_id, seven_days_ago_str))
        session_count = cursor.fetchone()["cnt"] or 0
        
        if session_count == 0:
            consistency_score = 0.0
        elif session_count == 1:
            consistency_score = 4.0
        elif session_count == 2:
            consistency_score = 7.0
        elif session_count == 3:
            consistency_score = 9.0
        else:
            consistency_score = 10.0
            
        cursor.execute("""
            SELECT s.avg_form_score
            FROM sets s
            JOIN exercises e ON s.exercise_id = e.exercise_id
            JOIN sessions sess ON e.session_id = sess.session_id
            WHERE sess.user_id = ? AND sess.date >= ? AND s.avg_form_score > 0
        """, (user_id, seven_days_ago_str))
        form_scores = [r["avg_form_score"] for r in cursor.fetchall()]
        
        avg_form_score = None
        if form_scores:
            avg_form_score = (sum(form_scores) / len(form_scores)) / 10.0
            
        goal = (profile.get("fitness_goal") or "").lower()
        if any(k in goal for k in ["loss", "cut", "deficit", "lean"]):
            target_balance = -400.0
        elif any(k in goal for k in ["gain", "bulk", "build", "mass"]):
            target_balance = 300.0
        else:
            target_balance = 0.0
            
        daily_balances = []
        for i in range(7):
            day_str = (today - datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            
            nutrition = db.get_nutrition_data(user_id, day_str)
            
            cursor.execute("SELECT SUM(total_calories_burned) as cal FROM sessions WHERE user_id = ? AND date = ?", (user_id, day_str))
            webcam_row = cursor.fetchone()
            webcam_cals = webcam_row["cal"] if (webcam_row and webcam_row["cal"]) else 0.0
            
            cursor.execute("SELECT SUM(calories_burned) as cal FROM cardio_logs WHERE user_id = ? AND date = ?", (user_id, day_str))
            cardio_row = cursor.fetchone()
            cardio_cals = cardio_row["cal"] if (cardio_row and cardio_row["cal"]) else 0.0
            
            exercise_burn = webcam_cals + cardio_cals
            
            if nutrition or exercise_burn > 0:
                consumed = nutrition["calories_consumed"] if nutrition else 0.0
                tef = consumed * 0.10
                bmr = calculate_bmr(weight, height, age, profile.get("sex", "unspecified"))
                net_cals = consumed - (exercise_burn + bmr + tef)
                
                dev = abs(net_cals - target_balance)
                day_score = max(0.0, 10.0 - (dev / 100.0) * 1.0)
                daily_balances.append(day_score)
                
        calorie_balance_score = None
        if daily_balances:
            calorie_balance_score = sum(daily_balances) / len(daily_balances)
            
        recent_prs = db.get_recent_prs_count(user_id, seven_days_ago_str)
        pr_progress_score = 10.0 if recent_prs > 0 else 0.0
    finally:
        conn.close()
    
    activity_components = {
        "consistency": round(consistency_score, 2),
        "pr_progress": round(pr_progress_score, 2)
    }
    
    base_weights = {
        "consistency": 0.35,
        "avg_form": 0.35,
        "calorie_balance": 0.15,
        "pr_progress": 0.15
    }
    
    avail_activity = {
        "consistency": consistency_score,
        "pr_progress": pr_progress_score
    }
    if avg_form_score is not None:
        avail_activity["avg_form"] = avg_form_score
        activity_components["avg_form"] = round(avg_form_score, 2)
    if calorie_balance_score is not None:
        avail_activity["calorie_balance"] = calorie_balance_score
        activity_components["calorie_balance"] = round(calorie_balance_score, 2)
        
    sum_weights = sum(base_weights[k] for k in avail_activity.keys())
    
    if sum_weights > 0:
        activity_score = sum(val * (base_weights[k] / sum_weights) for k, val in avail_activity.items())
    else:
        activity_score = None
        
    # --- Final Score combination ---
    if activity_score is not None:
        raw_final_score = 0.82 * lifestyle_avg + 0.18 * activity_score
        lifestyle_contribution = 0.82 * lifestyle_avg
        activity_contribution = 0.18 * activity_score
    else:
        raw_final_score = lifestyle_avg
        lifestyle_contribution = lifestyle_avg
        activity_contribution = 0.0
        
    final_score = max(1.00, min(10.00, raw_final_score))
    
    def get_letter_grade(s):
        if s >= 9.5: return "A+"
        elif s >= 9.0: return "A"
        elif s >= 8.5: return "A-"
        elif s >= 8.0: return "B+"
        elif s >= 7.5: return "B"
        elif s >= 7.0: return "B-"
        elif s >= 6.5: return "C+"
        elif s >= 6.0: return "C"
        elif s >= 5.5: return "C-"
        elif s >= 5.0: return "D+"
        elif s >= 4.5: return "D"
        elif s >= 4.0: return "D-"
        else: return "F"
        
    grade = get_letter_grade(final_score)
    
    return {
        "score": round(final_score, 2),
        "grade": grade,
        "breakdown": {
            "lifestyle": {
                "score": round(lifestyle_avg, 2),
                "contribution": round(lifestyle_contribution, 2),
                "components": lifestyle_components
            },
            "activity": {
                "score": round(activity_score, 2) if activity_score is not None else None,
                "contribution": round(activity_contribution, 2),
                "components": activity_components
            }
        },
        "missing_inputs": missing_inputs
    }

@app.get("/fitness-score")
def get_fitness_score(user_id: int = Depends(get_current_user_id)):
    try:
        return calculate_fitness_score_internal(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate fitness score: {str(e)}")

@app.get("/ai/coach-tip")
def get_coach_tip(user_id: int = Depends(get_current_user_id)):
    from ai.coach_client import get_groq_client
    try:
        sessions = db.get_recent_sessions(user_id, limit=10)
    except Exception as e:
        print(f"Error fetching recent sessions: {e}")
        return {"tip": "Coach tip unavailable right now"}

    if not sessions:
        return {"tip": "Log a workout first to get personalized coaching tips"}

    try:
        # Fetch user Fitness Score
        fit_score = calculate_fitness_score_internal(user_id)
        fit_score_str = f"Fitness Score: {fit_score['score']} ({fit_score['grade']})\n"
        fit_score_str += f"- Lifestyle sub-score: {fit_score['breakdown']['lifestyle']['score']}/10 (components: {fit_score['breakdown']['lifestyle']['components']})\n"
        if fit_score['breakdown']['activity']['score'] is not None:
            fit_score_str += f"- Activity sub-score: {fit_score['breakdown']['activity']['score']}/10 (components: {fit_score['breakdown']['activity']['components']})\n"
        else:
            fit_score_str += "- Activity sub-score: No activity logged in the last 7 days.\n"
        if fit_score['missing_inputs']:
            fit_score_str += f"- Missing inputs in profile: {', '.join(fit_score['missing_inputs'])}\n"

        session_summaries = []
        for s in sessions:
            ex_done = s.get("exercises_done") or "None"
            session_summaries.append(
                f"Date: {s['date']}, Exercises: {ex_done}, Sets: {s['total_sets']}, Reps: {s['total_reps']}, "
                f"Avg Form Score: {s['avg_form_score']:.1f}%, Calories Burned: {s['total_calories_burned']:.1f} kcal"
            )
        sessions_str = "\n".join(session_summaries)

        weight_history = db.get_weight_history(user_id, days=30)
        weight_trend_str = "No weight entries logged recently."
        if weight_history:
            first_w = weight_history[0]["weight_kg"]
            last_w = weight_history[-1]["weight_kg"]
            diff = last_w - first_w
            trend = "losing weight" if diff < 0 else "gaining weight" if diff > 0 else "maintaining weight"
            weight_trend_str = f"Weight History (last 30 days): starting {first_w:.1f} kg, current {last_w:.1f} kg (trend: {trend} of {abs(diff):.1f} kg)"

        prs = db.get_user_prs(user_id)
        prs_str_list = []
        for ex, pr_info in prs.items():
            details = []
            if "weight" in pr_info:
                details.append(pr_info["weight"])
            if "reps" in pr_info:
                details.append(pr_info["reps"])
            prs_str_list.append(f"{ex} ({' / '.join(details)})")
        prs_str = ", ".join(prs_str_list) if prs_str_list else "No personal records yet."

        summarized_data = (
            f"User Fitness Score Details:\n{fit_score_str}\n\n"
            f"Recent sessions:\n{sessions_str}\n\n"
            f"Weight trend: {weight_trend_str}\n\n"
            f"Personal Records (PRs): {prs_str}"
        )

        prompt = (
            f"Based on this user's recent workout data and health metrics:\n{summarized_data}\n\n"
            f"give one specific, encouraging, actionable coaching tip in 2-3 sentences. "
            f"Reference their computed Fitness Score and letter grade directly (e.g. 'Your fitness score is X (Y), driven mainly by...'), "
            f"and refer to something specific from their data rather than generic advice."
        )

        client = get_groq_client()
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
            timeout=10.0,
        )
        reply = chat_completion.choices[0].message.content.strip()
        if (reply.startswith('"') and reply.endswith('"')) or (reply.startswith("'") and reply.endswith("'")):
            reply = reply[1:-1].strip()
        return {"tip": reply}
    except Exception as e:
        print(f"Error calling Groq API for coach tip: {e}")
        return {"tip": "Coach tip unavailable right now"}

@app.get("/exercises")
def get_exercises():
    return [
        {
            "key": key,
            "display_name": val["display_name"],
            "category": val["category"],
            "mode": val.get("mode", "rep")
        }
        for key, val in EXERCISE_LIBRARY.items()
    ]

# ==================== AUTHENTICATION & ADMIN ENDPOINTS ====================

@app.post("/api/auth/register")
@limiter.limit("3/minute")
def register_user(data: models.UserRegisterRequest, request: Request):
    try:
        user_id = db.create_user(
            username=data.username,
            password=data.password,
            name=data.name
        )
        request.session["user_id"] = user_id
        return {"status": "success", "message": "User registered successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/login")
@limiter.limit("5/minute")
def login_user(data: models.UserLoginRequest, request: Request):
    user = db.authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    request.session["user_id"] = user["user_id"]
    return {"status": "success", "message": "Logged in successfully", "is_admin": bool(user["is_admin"])}

@app.post("/api/auth/logout")
def logout_user(request: Request):
    request.session.clear()
    return {"status": "success", "message": "Logged out successfully"}

@app.get("/api/auth/me")
def get_me(user_id: int = Depends(get_current_user_id)):
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "user_id": user["user_id"],
        "username": user["username"],
        "name": user["name"],
        "is_admin": bool(user["is_admin"])
    }

@app.get("/api/admin/users")
def get_admin_users(user_id: int = Depends(get_current_user_id)):
    user = db.get_user_by_id(user_id)
    if not user or not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Forbidden: Admin access required")
    return db.get_admin_users_summary()

@app.post("/set/log")
def log_set(data: models.SetLogRequest, user_id: int = Depends(get_current_user_id)):
    session_id = data.session_id
    if session_id is None:
        session_id = db.create_in_progress_session(user_id)
    else:
        # Verify ownership of session
        session_details = db.get_session_details(session_id, user_id)
        if not session_details:
            raise HTTPException(status_code=403, detail="Access denied to session.")
        
    if data.exercise_key not in EXERCISE_LIBRARY:
        raise HTTPException(status_code=400, detail=f"Invalid exercise: {data.exercise_key}")
        
    display_name = EXERCISE_LIBRARY[data.exercise_key]["display_name"]
    exercise_id = db.get_or_create_exercise(session_id, data.exercise_key, display_name)
    
    db.log_set_to_db(
        exercise_id=exercise_id,
        set_number=data.set_number,
        reps=data.reps_counted,
        weight=data.weight_kg,
        rpe=data.rpe,
        form_score=data.avg_form_score,
        pain_flag=data.pain_flag,
        pain_location=data.pain_location,
        duration_seconds=data.duration_seconds,
        weight_mode=data.weight_mode
    )
    return {"status": "success", "message": "Set logged successfully", "session_id": session_id}

@app.post("/session/end")
def end_session(data: models.SessionEndRequest, user_id: int = Depends(get_current_user_id)):
    session_details = db.get_session_details(data.session_id, user_id)
    if not session_details:
        raise HTTPException(status_code=403, detail="Access denied to session.")
        
    summary = db.finalize_session(data.session_id, notes=data.notes)
    if summary is None:
        raise HTTPException(status_code=400, detail="Invalid session ID or session not found.")
    return summary

@app.get("/sessions/recent")
def get_recent_sessions(user_id: int = Depends(get_current_user_id)):
    return db.get_recent_sessions(user_id)

@app.get("/sessions/{session_id}")
def get_session(session_id: int, user_id: int = Depends(get_current_user_id)):
    details = db.get_session_details(session_id, user_id)
    if not details:
        raise HTTPException(status_code=404, detail="Session not found.")
    return details

@app.get("/profile")
def get_profile(user_id: int = Depends(get_current_user_id)):
    profile = db.get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")
    return profile

@app.post("/profile")
def update_profile(data: models.ProfileRequest, user_id: int = Depends(get_current_user_id)):
    db.save_profile(
        user_id=user_id,
        name=data.name,
        age=data.age,
        weight=data.weight_kg,
        height=data.height_cm,
        sex=data.sex,
        fitness_goal=data.fitness_goal,
        gender=data.gender,
        diet_quality=data.diet_quality,
        stress_level=data.stress_level,
        sleep_hours=data.sleep_hours,
        smoker=data.smoker,
        exercise_freq=data.exercise_freq,
        alcohol_consumption=data.alcohol_consumption
    )
    return {"status": "success", "message": "Profile updated successfully"}

@app.post("/profile/change-password")
def change_password(data: models.PasswordChangeRequest, user_id: int = Depends(get_current_user_id)):
    user = db.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if not db.verify_password(data.current_password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Incorrect current password.")

    if data.new_password != data.confirm_new_password:
        raise HTTPException(status_code=400, detail="New passwords do not match.")

    # Update password hash
    new_hash = db.hash_password(data.new_password)
    db.update_user_password(user_id, new_hash)
    return {"status": "success", "message": "Password changed successfully."}

# --- Part 2 Weight Endpoints ---

@app.get("/weight/history")
def get_weight_history(days: Optional[str] = "90", user_id: int = Depends(get_current_user_id)):
    # If days is "all", it will pass days="all"
    return db.get_weight_history(user_id=user_id, days=days)

@app.post("/weight/log")
def log_weight_entry(data: models.WeightLogRequest, user_id: int = Depends(get_current_user_id)):
    db.log_weight(user_id=user_id, date=data.date, weight_kg=data.weight_kg)
    return {"status": "success", "message": "Weight logged successfully"}

# --- Part 2 Cardio Endpoints ---

@app.post("/cardio/log")
def log_cardio_entry(data: models.CardioLogRequest, user_id: int = Depends(get_current_user_id)):
    db.log_cardio(
        user_id=user_id,
        date=data.date,
        activity_name=data.activity_name,
        duration_mins=data.duration_mins,
        calories_burned=data.calories_burned,
        entry_method=data.entry_method
    )
    return {"status": "success", "message": "Cardio log saved successfully"}

@app.get("/cardio/{date}")
def get_cardio_date(date: str, user_id: int = Depends(get_current_user_id)):
    return db.get_cardio_logs(user_id=user_id, date=date)

# --- Part 2 Nutrition Endpoints ---

@app.post("/nutrition/log")
def log_nutrition_entry(data: models.NutritionLogRequest, user_id: int = Depends(get_current_user_id)):
    db.log_nutrition(
        user_id=user_id,
        date=data.date,
        calories_consumed=data.calories_consumed,
        protein=data.protein_g,
        carbs=data.carbs_g,
        fat=data.fat_g
    )
    return {"status": "success", "message": "Nutrition logs saved successfully"}

@app.get("/nutrition/{date}")
def get_nutrition_date(date: str, user_id: int = Depends(get_current_user_id)):
    profile = db.get_profile(user_id)
    return get_nutrition_breakdown_internal(user_id, date, profile)

# --- Part 2 Aggregation Dashboard ---

@app.get("/dashboard/today")
def get_dashboard_today(user_id: int = Depends(get_current_user_id)):
    today_str = datetime.now().strftime("%Y-%m-%d")
    profile = db.get_profile(user_id)
    nutrition = get_nutrition_breakdown_internal(user_id, today_str, profile)
    
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            COUNT(session_id) as session_count,
            SUM(total_sets) as total_sets,
            SUM(total_reps) as total_reps,
            AVG(avg_form_score) as avg_form_score,
            SUM(total_calories_burned) as total_calories_burned
        FROM sessions 
        WHERE user_id = ? AND date = ?
    """, (user_id, today_str))
    sess_row = cursor.fetchone()
    
    today_sessions = {
        "session_count": sess_row["session_count"] or 0,
        "total_sets": sess_row["total_sets"] or 0,
        "total_reps": sess_row["total_reps"] or 0,
        "avg_form_score": sess_row["avg_form_score"] or 100.0,
        "calories_burned": sess_row["total_calories_burned"] or 0.0
    }
    
    cursor.execute("SELECT weight_kg FROM weight_history WHERE user_id = ? AND date = ?", (user_id, today_str))
    weight_row = cursor.fetchone()
    current_weight = weight_row["weight_kg"] if weight_row else (profile["weight_kg"] if profile else 75.0)
    
    conn.close()
    
    return {
        "date": today_str,
        "profile": profile,
        "nutrition": nutrition,
        "sessions": today_sessions,
        "current_weight": current_weight
    }

# ==================== WEBSOCKET ====================

def process_and_draw_frame(detector, counter, frame):
    height, width = frame.shape[:2]
    
    # Perform pose detection
    results = detector.process_frame(frame)
    landmarks_dict = detector.get_landmarks_dict(results)
    
    current_angles = {}
    
    if landmarks_dict:
        # 1. Compute angles dynamically
        angles_config = counter.config.get("angles", {})
        for angle_name, joints in angles_config.items():
            if all(j in landmarks_dict for j in joints):
                pt_a = landmarks_dict[joints[0]]
                pt_b = landmarks_dict[joints[1]]
                pt_c = landmarks_dict[joints[2]]
                current_angles[angle_name] = calculate_angle(pt_a, pt_b, pt_c)
        
        # 2. Update counter state machine
        counter.update(current_angles, landmarks_dict)
        
        # 3. Draw skeleton
        frame = detector.draw_skeleton(frame, results)
        
        # 4. Overlay angles at joint vertices
        for angle_name, joints in angles_config.items():
            if angle_name in current_angles:
                vertex_joint = joints[1]
                if vertex_joint in landmarks_dict:
                    pt_vertex = landmarks_dict[vertex_joint]
                    px = int(pt_vertex[0] * width)
                    py = int(pt_vertex[1] * height)
                    cv2.putText(
                        frame,
                        f"{int(current_angles[angle_name])}deg",
                        (px + 10, py - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.45,
                        (255, 255, 255),
                        1,
                        cv2.LINE_AA
                    )
    else:
        # Signal tracking loss to the counter to reset time tracking
        counter.update({}, {})
        
        # Overlay warning in red on the frame center
        (tw, th), _ = cv2.getTextSize("TRACKING LOST - PAUSED", cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        tx = (width - tw) // 2
        ty = (height - th) // 2
        cv2.rectangle(frame, (tx - 15, ty - 25), (tx + tw + 15, ty + 15), (0, 0, 0), -1)
        cv2.rectangle(frame, (tx - 15, ty - 25), (tx + tw + 15, ty + 15), (68, 23, 255), 2)
        cv2.putText(frame, "TRACKING LOST - PAUSED", (tx, ty - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (68, 23, 255), 2, cv2.LINE_AA)
        
        # Prepend tracking lost warning to feedback list
        tracking_feedback = {"message": "Pose lost - reposition yourself", "severity": "YELLOW"}
        if not any(f["message"] == tracking_feedback["message"] for f in counter.latest_feedback):
            counter.latest_feedback = [tracking_feedback] + counter.latest_feedback
                    
    # Overlay HUD elements
    # 1. Reps / Hold timer (top-right)
    if counter.mode == "hold":
        # Running timer display
        min_sec = f"{counter.reps_counted // 60:02d}:{counter.reps_counted % 60:02d}"
        cv2.putText(frame, "HOLD TIME", (width - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (170, 170, 170), 1, cv2.LINE_AA)
        cv2.putText(frame, min_sec, (width - 150, 85), cv2.FONT_HERSHEY_DUPLEX, 1.6, (0, 200, 83), 3, cv2.LINE_AA)
    else:
        cv2.putText(frame, "REPS", (width - 120, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (170, 170, 170), 1, cv2.LINE_AA)
        cv2.putText(frame, str(counter.reps_counted), (width - 120, 85), cv2.FONT_HERSHEY_DUPLEX, 1.8, (0, 200, 83), 3, cv2.LINE_AA)
    
    # 2. Stage
    stage_str = (counter.stage or "--").upper()
    cv2.putText(frame, f"STAGE: {stage_str}", (width - 150, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
    
    # 3. Feedback Badges
    y_offset = 20
    for fb in counter.latest_feedback[:2]:
        msg = fb["message"]
        sev = fb["severity"]
        
        if sev == "RED":
            bg_color = (68, 23, 255)
            text_color = (255, 255, 255)
        elif sev == "YELLOW":
            bg_color = (0, 214, 255)
            text_color = (0, 0, 0)
        else:
            bg_color = (83, 200, 0)
            text_color = (255, 255, 255)
            
        (text_w, text_h), _ = cv2.getTextSize(msg, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
        cv2.rectangle(frame, (15, y_offset), (25 + text_w + 10, y_offset + 25), bg_color, -1)
        cv2.rectangle(frame, (15, y_offset), (25 + text_w + 10, y_offset + 25), (44, 44, 44), 1)
        cv2.putText(frame, msg, (23, y_offset + 17), cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, 1, cv2.LINE_AA)
        y_offset += 32
        
    # 4. Form Score Bar
    bar_x1, bar_y1 = 40, height - 30
    bar_x2, bar_y2 = width - 40, height - 20
    cv2.rectangle(frame, (bar_x1, bar_y1), (bar_x2, bar_y2), (40, 40, 40), -1)
    
    score_width = int((bar_x2 - bar_x1) * (counter.avg_form_score / 100.0))
    if counter.avg_form_score >= 75:
        fill_color = (83, 200, 0)
    elif counter.avg_form_score >= 50:
        fill_color = (0, 214, 255)
    else:
        fill_color = (68, 23, 255)
    cv2.rectangle(frame, (bar_x1, bar_y1), (bar_x1 + score_width, bar_y2), fill_color, -1)
    cv2.putText(
        frame,
        f"AVG FORM SCORE: {int(counter.avg_form_score)}%",
        (bar_x1, bar_y1 - 8),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (255, 255, 255),
        1,
        cv2.LINE_AA
    )
    
    out_base64 = encode_frame_to_base64(frame)
    return out_base64, current_angles

@app.websocket("/ws/workout")
async def websocket_workout(websocket: WebSocket):
    user_id = websocket.session.get("user_id")
    if not user_id:
        await websocket.accept()
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    
    detector = PoseDetector()
    counter = None
    ping_task = None
    
    try:
        async def send_pings():
            try:
                while True:
                    await asyncio.sleep(10)
                    await websocket.send_json({"type": "ping"})
            except Exception:
                pass

        ping_task = asyncio.create_task(send_pings())
        loop = asyncio.get_running_loop()
        
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "pong":
                continue
                
            frame_data = data.get("frame")
            exercise_key = data.get("exercise")
            
            if not frame_data or not exercise_key:
                continue
                
            frame = decode_base64_frame(frame_data)
            if frame is None:
                continue
                
            # Lazily initialize counter when exercise changes
            if counter is None or counter.exercise_key != exercise_key:
                ex_config = EXERCISE_LIBRARY.get(exercise_key)
                if not ex_config:
                    continue
                counter = RepCounter(exercise_key, ex_config)
                
                # Restore reps count if reconnecting mid-set
                current_reps = data.get("current_reps", 0)
                if current_reps > 0:
                    counter.reps_counted = current_reps
                
            # Offload heavy rendering, pose detection and base64 encoding to thread pool
            out_base64, current_angles = await loop.run_in_executor(
                pose_executor,
                process_and_draw_frame,
                detector,
                counter,
                frame
            )
            
            response = {
                "frame": out_base64,
                "reps": counter.reps_counted,
                "form_score": counter.avg_form_score,
                "stage": counter.stage,
                "feedback": counter.latest_feedback,
                "angles": current_angles
            }
            await websocket.send_json(response)
            
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"Exception in WebSocket handler: {e}")
    finally:
        if ping_task:
            ping_task.cancel()
        try:
            await websocket.close()
        except:
            pass

@app.get("/")
def read_root(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login.html")
    return RedirectResponse(url="/overview")

@app.get("/overview")
def read_overview(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login.html")
    return FileResponse("static/overview.html")

@app.get("/workout")
def read_workout(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login.html")
    return FileResponse("static/workout.html")

@app.get("/history")
def read_history(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login.html")
    return FileResponse("static/history.html")

@app.get("/profile-page")
def read_profile_page(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login.html")
    return FileResponse("static/profile.html")

@app.get("/calculator")
def read_calculator_page(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login.html")
    return FileResponse("static/calculator.html")

@app.post("/experimental/risk-estimate")
@limiter.limit("10/minute")
def risk_estimate(request: Request, data: models.RiskEstimateRequest, user_id: int = Depends(get_current_user_id)):
    from ml_models.predictor import predict_risk

    profile = db.get_profile(user_id) or {}
    
    required_keys = [
        "age",
        "gender",
        "height_cm",
        "weight_kg",
        "smoker",
        "diet_quality",
        "stress_level",
        "sleep_hours",
        "exercise_freq",
        "alcohol_consumption"
    ]
    
    features = {}
    missing_fields = []
    
    # Prioritize request body values, fallback to database profile values
    for key in required_keys:
        val = getattr(data, key)
        if val is not None:
            features[key] = val
        else:
            db_val = profile.get(key)
            # Match sex to gender if gender is not set
            if key == "gender" and (db_val is None or db_val == ""):
                db_val = profile.get("sex")
                if db_val == "unspecified":
                    db_val = None
                    
            if db_val is not None and db_val != "":
                features[key] = db_val
            else:
                missing_fields.append(key)
                
    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required fields for risk estimation: {', '.join(missing_fields)}"
        )
        
    # Calculate BMI on the fly if not provided
    bmi = data.bmi
    if bmi is None or bmi <= 0.0:
        height_cm = features.get("height_cm")
        weight_kg = features.get("weight_kg")
        if height_cm is None or height_cm == 0 or weight_kg is None:
            bmi = None
        else:
            height_m = height_cm / 100.0
            if height_m == 0:
                bmi = None
            else:
                bmi = weight_kg / (height_m ** 2)
    features["bmi"] = bmi

    try:
        result = predict_risk(features)
        return {
            "predicted_probability": result["risk_probability"],
            "predicted_class": result["predicted_class"],
            "confidence_note": (
                "This model showed no meaningful correlation between inputs and outcome "
                "during training (max |r| = 0.03) — treat this as exploratory only, "
                "not a real health assessment."
            )
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model execution failed: {str(e)}")

@app.get("/admin")
def read_admin(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login.html")
    user = db.get_user_by_id(user_id)
    if not user or not user.get("is_admin"):
        return HTMLResponse("<html><body><h1>Access Denied</h1><p>You must be an admin to view this page.</p></body></html>", status_code=403)
    return FileResponse("static/admin/admin.html")

# Mount static folder last
app.mount("/", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
