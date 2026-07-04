# FitSense AI — Part 1: Core Engine & Data-Driven Exercise System

FitSense AI is a next-generation fitness web application that uses computer vision to track body posture, count exercise repetitions, score movement form in real-time, and log detailed workout statistics.

This repository implements the robust, data-driven core engine (Part 1 of a 2-part build) which is designed to scale dynamically from 3 to 50 exercises with zero code changes.

---

## 🛠️ Tech Stack
- **Backend:** FastAPI + Python 3.11
- **Pose Detection:** MediaPipe Pose
- **Video Processing:** OpenCV
- **Database:** SQLite
- **Frontend:** HTML5 + Vanilla CSS + JavaScript
- **Streaming:** WebSockets

---

## 📂 File Structure
```
fitsense-ai/
  main.py                 — FastAPI application & WebSocket handlers
  config/
    exercise_library.py   — Single source of truth config (all exercise definitions)
  database/
    db.py                 — SQLite queries, table creations & migrations
    models.py             — Pydantic schemas for endpoint request validations
  pose/
    detector.py           — MediaPipe initialization & stable vector math angles calculations
    counter.py            — Generic state machine & form evaluator (parameterized by config)
  static/
    index.html            — Dashboard layout
    style.css             — Custom premium dark theme style system
    app.js                — Camera capturer, WebSocket streaming loop & REST integrations
  requirements.txt        — Dependencies list
  README.md               — Project documentation
```

---

## 🚀 Setup & Launching

1. **Install Dependencies:**
   Ensure you have Python 3.11 installed. In your terminal, run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Backend Server:**
   Launch the FastAPI application:
   ```bash
   python main.py
   ```
   Alternatively, you can run:
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

3. **Access the Web Dashboard:**
   Open your browser and navigate to:
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 Verification Checklists

### 1. Dynamic Exercises Configuration
- On application load, the frontend makes a `GET /exercises` call.
- The dropdown list is dynamically generated displaying **Squat**, **Pushup**, and **Bicep Curl** categorized cleanly.

### 2. Rep Counter & Stage Machine
- Selecting an exercise sets up its thresholds and primary angles.
- **Squats/Pushups:** Down threshold = 90°, Up threshold = 160°. Transitioning under 90° sets stage to `DOWN`. Climbing above 160° registers 1 rep, changes stage to `UP`, evaluates form, and resets internal rep-stats.
- **Bicep Curls:** Down threshold = 150° (arms extended), Up threshold = 40° (arms curled). Transitioning under 40° registers 1 rep, changes stage to `UP`. Straightening arms back above 150° resets stage to `DOWN`.

### 3. SQLite DB Integrity
- The system automatically creates `fitsense.db` upon initial launch.
- If the `users` table is empty, a default athlete is added.
- Logging sets and ending sessions updates rows in `sessions`, `exercises`, and `sets` respectively.
- Session summary list is reloaded from `GET /sessions/recent` and clicking "View Detail" retrieves complete set-by-set parameters.
