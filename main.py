import base64
import cv2
import numpy as np
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from config.exercise_library import EXERCISE_LIBRARY
from database import db, models
from pose.detector import PoseDetector, calculate_angle
from pose.counter import RepCounter

# Lifespan manager for FastAPI
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database and insert default user
    db.init_db()
    yield

app = FastAPI(title="FitSense AI Core Engine", lifespan=lifespan)

# Global active session tracking (MVP-scoped)
current_session_id = None

def decode_base64_frame(base64_str: str) -> np.ndarray:
    """
    Decodes a base64 encoded string into an OpenCV BGR image.
    Handles data URI prefixes if present.
    """
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
    """
    Encodes an OpenCV image to a base64 string.
    """
    try:
        _, buffer = cv2.imencode('.jpg', frame)
        base64_str = base64.b64encode(buffer).decode('utf-8')
        return base64_str
    except Exception as e:
        print(f"Error encoding frame: {e}")
        return ""

@app.get("/exercises")
def get_exercises():
    """
    Returns configured exercises from EXERCISE_LIBRARY dynamically.
    Used by frontend to populate exercise options dropdown.
    """
    return [
        {
            "key": key,
            "display_name": val["display_name"],
            "category": val["category"]
        }
        for key, val in EXERCISE_LIBRARY.items()
    ]

@app.post("/set/log")
def log_set(data: models.SetLogRequest):
    """
    Logs details of a completed workout set.
    Creates an active session on the fly if none is in progress.
    """
    global current_session_id
    if current_session_id is None:
        current_session_id = db.create_in_progress_session()
        
    if data.exercise_key not in EXERCISE_LIBRARY:
        raise HTTPException(status_code=400, detail=f"Invalid exercise key: {data.exercise_key}")
        
    display_name = EXERCISE_LIBRARY[data.exercise_key]["display_name"]
    
    # Fetch or create the exercise entry associated with this session
    exercise_id = db.get_or_create_exercise(current_session_id, data.exercise_key, display_name)
    
    # Save the set record to DB
    db.log_set_to_db(
        exercise_id=exercise_id,
        set_number=data.set_number,
        reps=data.reps_counted,
        weight=data.weight_kg,
        rpe=data.rpe,
        form_score=data.avg_form_score,
        pain_flag=data.pain_flag,
        pain_location=data.pain_location
    )
    
    return {"status": "success", "message": "Set logged successfully"}

@app.post("/session/end")
def end_session(data: models.SessionEndRequest):
    """
    Finalizes the currently active workout session.
    """
    global current_session_id
    if current_session_id is None:
        raise HTTPException(status_code=400, detail="No active workout session to end.")
        
    summary = db.finalize_session(current_session_id, notes=data.notes)
    current_session_id = None
    return summary

@app.get("/sessions/recent")
def get_recent_sessions():
    """
    Returns details of the last 10 workout sessions.
    """
    return db.get_recent_sessions()

@app.get("/sessions/{session_id}")
def get_session(session_id: int):
    """
    Returns full metadata and logged sets for a specific session ID.
    """
    details = db.get_session_details(session_id)
    if not details:
        raise HTTPException(status_code=404, detail="Session not found.")
    return details

@app.websocket("/ws/workout")
async def websocket_workout(websocket: WebSocket):
    await websocket.accept()
    
    detector = PoseDetector()
    counter = None
    
    try:
        while True:
            # Receive package
            data = await websocket.receive_json()
            frame_data = data.get("frame")
            exercise_key = data.get("exercise")
            
            if not frame_data or not exercise_key:
                continue
                
            frame = decode_base64_frame(frame_data)
            if frame is None:
                continue
                
            height, width = frame.shape[:2]
            
            # Lazily initialize/switch counter for selected exercise
            if counter is None or counter.exercise_key != exercise_key:
                ex_config = EXERCISE_LIBRARY.get(exercise_key)
                if not ex_config:
                    continue
                counter = RepCounter(exercise_key, ex_config)
                
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
                
                # 2. Update rep counting state machine
                counter.update(current_angles, landmarks_dict)
                
                # 3. Draw pose skeleton
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
                            
            # Draw HUD Overlays (even if no pose is detected to maintain UI structure)
            # 1. Reps count (top-right)
            cv2.putText(frame, "REPS", (width - 120, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (170, 170, 170), 1, cv2.LINE_AA)
            cv2.putText(frame, str(counter.reps_counted), (width - 120, 85), cv2.FONT_HERSHEY_DUPLEX, 1.8, (0, 200, 83), 3, cv2.LINE_AA)
            
            # 2. Stage indicator
            stage_str = (counter.stage or "--").upper()
            cv2.putText(frame, f"STAGE: {stage_str}", (width - 150, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
            
            # 3. Feedback Badge stack (top-left)
            y_offset = 20
            for fb in counter.latest_feedback[:2]:
                msg = fb["message"]
                sev = fb["severity"]
                
                if sev == "RED":
                    bg_color = (68, 23, 255) # BGR
                    text_color = (255, 255, 255)
                elif sev == "YELLOW":
                    bg_color = (0, 214, 255) # BGR
                    text_color = (0, 0, 0)
                else:
                    bg_color = (83, 200, 0) # BGR
                    text_color = (255, 255, 255)
                    
                (text_w, text_h), _ = cv2.getTextSize(msg, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
                cv2.rectangle(frame, (15, y_offset), (25 + text_w + 10, y_offset + 25), bg_color, -1)
                cv2.rectangle(frame, (15, y_offset), (25 + text_w + 10, y_offset + 25), (44, 44, 44), 1)
                cv2.putText(frame, msg, (23, y_offset + 17), cv2.FONT_HERSHEY_SIMPLEX, 0.4, text_color, 1, cv2.LINE_AA)
                y_offset += 32
                
            # 4. Form Score Bar (bottom)
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
            
            # Encode frame back to Base64
            out_base64 = encode_frame_to_base64(frame)
            
            # Send payload back to frontend
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
        try:
            await websocket.close()
        except:
            pass

# Serve static files at root
# Place this last so API routes are matched first
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
