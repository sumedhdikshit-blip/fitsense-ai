import base64
import cv2
import numpy as np
import asyncio
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime
from typing import Optional

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

app = FastAPI(title="FitSense AI Core Engine", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key="fitsense_secret_session_key_123")

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
    cursor = conn.cursor()
    
    # Sum webcam sessions calories on this day
    cursor.execute("SELECT SUM(total_calories_burned) as cal FROM sessions WHERE user_id = ? AND date = ?", (user_id, date_str))
    webcam_row = cursor.fetchone()
    webcam_cals = webcam_row["cal"] if (webcam_row and webcam_row["cal"]) else 0.0
    
    # Sum cardio logs calories on this day
    cursor.execute("SELECT SUM(calories_burned) as cal FROM cardio_logs WHERE user_id = ? AND date = ?", (user_id, date_str))
    cardio_row = cursor.fetchone()
    cardio_cals = cardio_row["cal"] if (cardio_row and cardio_row["cal"]) else 0.0
    
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
        fitness_goal=data.fitness_goal
    )
    return {"status": "success", "message": "Profile updated successfully"}

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

@app.websocket("/ws/workout")
async def websocket_workout(websocket: WebSocket):
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
                
            height, width = frame.shape[:2]
            
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
