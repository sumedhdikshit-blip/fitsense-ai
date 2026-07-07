# FitSense AI — Core Engine & Data-Driven Health System

FitSense AI is a developer-focused fitness web application that integrates real-time computer vision pose estimation, manual workout logging, and complex metabolic energy calculators into a unified developer dashboard. Designed as a robust showcase of clean web design, parallel processing, and data-driven intelligence, it enables users to track movement accuracy, plan caloric goals, and compile custom, data-specific AI insights.

---

## 🛠️ Tech Stack

*   **Backend Framework:** FastAPI (ASGI) + Python 3.11+
*   **Computer Vision:** MediaPipe Pose + OpenCV (running in parallel background thread-pools)
*   **Database Engine:** SQLite (configured with multi-table relationships, index optimizations, and programmatic migrations)
*   **Machine Learning:** Scikit-Learn + XGBoost + CatBoost (Ensemble Classifier)
*   **AI Integrations:** Groq SDK (`llama-3.1-8b-instant`)
*   **Rate Limiting:** SlowAPI (Token-bucket rate limits per client IP)
*   **Logging:** Python standard `logging` + `RotatingFileHandler` (app.log rotating at 5MB)
*   **Frontend UI:** Responsive HTML5 + Vanilla CSS + Modular JavaScript (Glassmorphic dark-theme)
*   **Real-time Streaming:** ASGI WebSockets (frame-by-frame base64 coordinate streaming)

---

## 📂 Project Structure

```
fitsense-ai/
  main.py                 — FastAPI application routing, rate limiting, logging, and WS handlers
  requirements.txt        — Python dependencies list
  run_tests.py            — Custom automated test runner suite
  TRADEOFFS.md            — Documentation on technical simplifications and trade-offs
  config/
    exercise_library.py   — Config-driven library defining 50+ exercises and MET constants
  database/
    db.py                 — Database connector, query layer, index definitions, and migrations
    models.py             — Pydantic request/response data validation schemas
  ml/
    data/                 — Dataset storage directory (synthetic health/lifestyle logs)
    training/             — Scripts for training the experimental risk ML model
  ml_models/
    predictor.py          — ML classifier execution logic and feature scaling
    chronic_disease_ensemble_model.pkl — Trained classifier weights
    scaler.pkl            — Feature scaler artifact
  pose/
    detector.py           — MediaPipe joint angle calculations
    counter.py            — Generic state machine tracking repetitions and hold durations
  static/
    app-shared.js         — Shared authentication, navigation, and user context script
    overview.html / js    — Dashboard net calorie tracking, weight history charts, and AI Insights
    workout.html / js     — Webcam repetition tracker & manual logging controls
    history.html / js     — Past workouts & detailed set histories
    profile.html / js     — User profile metrics & password settings panel
    calculator.html / js  — Standalone metabolic BMR/TEF/NEAT/TDEE calculator
    login.html            — Secure credential entry login
    register.html         — New user account registration
    admin/
      admin.html / js     — Global admin diagnostic dashboard page
```

---

## 🚀 Setup & Launching

### 1. Install Dependencies
Ensure you have Python 3.11+ installed. In your terminal, run:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory (automatically excluded from version control):
```env
# Secret key for encrypting cookie-based user sessions (Required)
SESSION_SECRET=your-secure-random-secret-key-here

# API Key for generating AI Coach Tips and Deep Insights (Optional - falls back to mock)
GROQ_API_KEY=gsk_your-actual-groq-api-key-here
```
*(Note: If `SESSION_SECRET` is missing at launch, the application will raise a startup error and halt).*

### 3. Start the Backend Server
Launch the FastAPI application:
```bash
python main.py
```
Alternatively, run with Uvicorn directly:
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### 4. Access the Web Dashboard
Open your browser and navigate to:
[http://127.0.0.1:8000](http://127.0.0.1:8000)

*   **Default Local Account:** Username: `athlete` / Password: `athlete` *(Note: This default account is intended for local testing only. Change these credentials immediately on deployment).*

---

## 🧪 Key Features & Functionality

### 1. Real-time Webcam Pose Detection
*   Streams video frames from the webcam to the backend via WebSockets.
*   MediaPipe Pose analyzes joint coordinates (shoulders, hips, knees, elbows, ankles).
*   RepCounters run state-machine rules to count repetitions and measure hold times.
*   Draws joint markers, connection bones, active feedback labels, and a live form score bar overlay directly onto the stream.

### 2. Manual Workout Logging
*   Features a camera-free logging interface.
*   Users can quickly record set metrics (weight, reps, RPE, pain markers) to the database without webcam capture.
*   Saves manual logs with an `avg_form_score = 0.0` which are excluded from session and exercise averages to prevent diluting webcam form accuracy records.

### 3. Comprehensive 50+ Exercise Library
*   Config-driven configuration inside `config/exercise_library.py` covering exercises across major muscle groups.
*   Supports different joint counting tracking rules (e.g. angle checking at knees, hips, or elbows) and hold-duration constraints.
*   Provides MET constants for each exercise to compute task-specific calorie expenditure dynamically.

### 4. Session Tracking & Admin Dashboard
*   Full cookie-based session authentication with password hashing (SHA-256 with salts).
*   Features a Change Password interface enforcing a secure 8-character minimum.
*   Admin dashboard (restricted via role checking to `is_admin = 1` users) summarizing system statistics, active users, and system diagnostics.

### 5. Metabolic Tracking (Weight, Cardio, Nutrition)
*   **Weight Tracking:** Logs weight records to `weight_history`, dynamically updating weight trend progress charts (7D/30D/90D/All views).
*   **Cardio Logging:** Allows users to log cardio activities (preset or custom MET values) to calculate active calories burned.
*   **Nutrition Logging:** Logs daily macro and calorie ingestion. Multi-meal entries logged on the same day accumulate macros instead of overwriting.

### 6. Standalone Energy Calculator
*   Models energy calculations:
    *   **BMI:** Calculated based on profile weight and height.
    *   **BMR (Basal Metabolic Rate):** Mifflin-St Jeor formula mapping.
    *   **TEF (Thermic Effect of Food):** Evaluated as 10% of total daily calorie intake.
    *   **NEAT (Non-Exercise Activity Thermogenesis):** Estimated based on lifestyle activity levels.
    *   **TDEE (Total Daily Energy Expenditure):** Aggregated energy consumption baseline.
*   Allows comparison of current profile metrics with customized target inputs.

### 7. Computed Fitness Score
*   Calculates a dynamic score from 1.00 to 10.00 (mapped to letters A+ to F) on a daily basis:
    *   **82% Weight — Lifestyle Factors:** Evaluates age correctness, stress levels, sleep hygiene, and clinical BMI ranges.
    *   **18% Weight — Activity Factors:** Evaluates weekly workout consistency (sessions logged), webcam form scores, caloric balance, and new PR counts.
*   *If specific inputs (e.g., sleep, stress) are missing, the formula dynamically redistributes weights to avoid penalizing the user.*

### 8. AI Coach Tip & Deep Insights
*   **AI Coach Tip:** Generates a 2-3 sentence quick tip based on recent workouts.
*   **AI Deep Insights:** Renders a 5-card grid summarizing:
    1.  *Progress Summary:* Data-specific compilation of workout volumes and form scores.
    2.  *Tips to Improve:* Actionable advice on progressive overload.
    3.  *What to Avoid:* Cautions on joint stress or high RPE levels.
    4.  *Next Steps:* Concrete training directions.
    5.  *Motivation Note:* Encouraging, data-driven check-in.
*   *Runs Groq completions (`llama-3.1-8b-instant`) with strict JSON output schemas, a 5.0-second timeout budget, and single-retry cleaning to strip markdown fences.*

### 9. Experimental ML Chronic Disease Risk Model
*   Accessible on the profile page. Predicts risk indicators using an ensemble classifier (XGBoost + CatBoost + Scikit-Learn).
*   **Honesty & Caveats:** Explicitly caveated in the UI that the model was trained on a dataset displaying a maximum correlation of only $|r| \le 0.03$. It uses a low classification threshold of `10%` to mark risk as "Elevated," meaning it serves purely as a demonstration of pipeline deployment and feature scaling rather than clinical advice.

---

## 🏛️ Architecture & Reliability

*   **Config-Driven Exercises:** Exercise joint-checking rules are read dynamically from a schema, allowing developers to add new movements by editing a config array.
*   **Thread-Pool Offloading:** MediaPipe coordinate computations and OpenCV overlay rendering run inside a dedicated background thread-pool executor (`ThreadPoolExecutor`), keeping the FastAPI async loop responsive.
*   **Database Indexing:** Created SQLite indexes (`idx_sessions_user_date`, `idx_exercises_session`, `idx_sets_exercise`) to speed up history lookups and prevent N+1 query overhead.
*   **IP-Based Rate Limiting:** Rate limits are applied to the AI endpoints per client IP (5/min for Coach Tip, 3/min for Deep Insights) to prevent token abuse.
*   **Structured Logging:** Standardized Python logs write to stdout and `logs/app.log` (rotating at 5MB, keeping 3 backups) mapping timestamp, level, module name, and traces.

---

## 🧪 Testing Suite

The codebase features a custom automated test suite that validates db constraints, password verification, form logic, chart ranges, and AI fallback states.

To execute the tests:
```bash
python run_tests.py
```
*   **Current Test Count:** 23 tests passing.

---

## ⚠️ Known Limitations

*   **Single-User Focus:** Although multi-user authentication is supported, data isolation is local-first, and charts/scores are targeted at single athlete dashboards.
*   **SQLite Storage:** Optimized for low latency on local systems; not intended for high-concurrency production scales.
*   **Exploratory ML:** The disease risk model is purely demonstrative.
*   **Metabolic Estimates:** NEAT and TEF metrics are based on standard metabolic formulas and represent estimates, not laboratory-grade metabolic metrics.
