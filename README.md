# FitSense AI — Core Engine & Data-Driven Health System

FitSense AI is a next-generation fitness web application that uses computer vision to track body posture, count exercise repetitions, score movement form in real-time, log detailed workout statistics, and predict chronic disease risk based on lifestyle metrics.

---

## 🛠️ Tech Stack
- **Backend:** FastAPI + Python 3.11
- **Pose Detection:** MediaPipe Pose
- **Video Processing:** OpenCV
- **Database:** SQLite
- **Machine Learning:** Scikit-Learn + XGBoost + CatBoost (Ensemble Classifier)
- **Frontend:** HTML5 + Vanilla CSS + JavaScript
- **Streaming:** WebSockets

---

## 📂 File Structure
```
fitsense-ai/
  main.py                 — FastAPI application, API endpoints & WebSocket handlers
  chronic_disease_pipeline_final.py — ML model training pipeline
  synthetic_health_lifestyle.csv — Health metrics dataset
  config/
    exercise_library.py   — Definition of all exercises & their MET scores
  database/
    db.py                 — SQLite queries, table creations & migrations
    models.py             — Pydantic validation schemas
  pose/
    detector.py           — MediaPipe vector calculations for joints
    counter.py            — Generic state machine for reps & hold times
  static/
    app-shared.js         — Shared authentication, navigation, and user context
    overview.html / js    — Dashboard calorie counters & weight tracking charts
    workout.html / js     — Webcam repetition counter & manual logging controls
    history.html / js     — Past workouts & detailed set histories
    profile.html / js     — Dynamic user details & BMR configuration card
    login.html            — Secure credential login & admin redirect
    admin/
      admin.html / js     — Global admin diagnostic dashboard
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

## 🧪 Key Features & Verification

### 1. Split-Page Navigation
- The main app is organized into four clean pages: **Overview**, **Workout**, **History**, and **Profile**.
- A persistent, highlighted navigation bar coordinates moving between pages.

### 2. Manual Workout Logging
- In the **Workout** page, users can log workouts without using a webcam.
- Selecting an exercise, sets count, reps per set, RPE, and weight (with an explicit toggle for "total" vs "per side") maps data onto the same SQLite tables without faking form scores.

### 3. Chronic Disease Risk Prediction
- Users can train a custom ensemble model using the training pipeline.
- In the **Profile** page, users can calculate exploratory risk estimates using the 'Experimental: Chronic Disease Risk Model' card, which pulls user parameters from the database.

