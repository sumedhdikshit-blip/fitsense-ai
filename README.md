# FitSense AI — Core Engine & Data-Driven Health System

FitSense AI is a developer-focused fitness web application that combines computer vision pose-estimation, manual logging tools, and data-driven metabolic calculators into a unified web portal.

---

## 🛠️ Tech Stack
- **Backend:** FastAPI + Python 3.11
- **Pose Detection:** MediaPipe Pose
- **Video Processing:** OpenCV
- **Database:** SQLite (with parameterized queries and table migrations)
- **Machine Learning:** Scikit-Learn + XGBoost + CatBoost (Ensemble Classifier)
- **Rate Limiting:** SlowAPI (Token-bucket limiter)
- **Frontend:** HTML5 + Vanilla CSS + JavaScript
- **Streaming:** WebSockets for frame-by-frame coordinate tracking

---

## 📂 File Structure
```
fitsense-ai/
  main.py                 — FastAPI application, API endpoints & WebSocket handlers
  requirements.txt        — Python dependencies list
  config/
    exercise_library.py   — Definition of all exercises, categories, and MET values
  database/
    db.py                 — SQLite queries, database initialization, and table migrations
    models.py             — Pydantic request/response validation schemas
  ml/
    data/                 — Dataset storage folder (synthetic health/lifestyle logs)
    training/             — Scripts for ML model training pipelines
  ml_models/
    predictor.py          — Risk score probability classifier logic & feature scaling
    chronic_disease_ensemble_model.pkl — Trained classifier model weights
    scaler.pkl            — Training pipeline feature scaler
  pose/
    detector.py           — Joint angle coordinate calculations via MediaPipe
    counter.py            — Generic state machine for counting reps and hold durations
  static/
    app-shared.js         — Shared authentication, navigation, and user context script
    overview.html / js    — Dashboard net calorie tracking & weight history charts
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

1. **Install Dependencies:**
   Ensure you have Python 3.11+ installed. In your terminal, run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables:**
   Set the session secret key (highly recommended in production):
   * **PowerShell:** `$env:SESSION_SECRET="your-secure-key"`
   * **CMD:** `set SESSION_SECRET=your-secure-key`
   * **Linux/macOS:** `export SESSION_SECRET="your-secure-key"`

3. **Start the Backend Server:**
   Launch the FastAPI application:
   ```bash
   python main.py
   ```
   Alternatively, you can run:
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

4. **Access the Web Dashboard:**
   Open your browser and navigate to:
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

   * **Default Athlete Account:** Username: `athlete` / Password: `athlete` *(Note: This default account is intended for local testing and development environments only. For any public deployment, change this credential immediately).*

---

## 🧪 Key Features & Architecture

### 1. Split-Page Navigation
The frontend is decoupled into five distinct functional areas accessible from a unified navigation header:
- **Overview (`/overview`)**: Consolidates daily calorie ingestion, cardio outputs, resting BMR/TEF values, and draws dynamic weight-change progress graphs.
- **Workout (`/workout`)**: Runs real-time computer vision repetition tracking via WebSockets and features a robust manual entry logging modal (allowing sets to be logged directly to the DB without pose tracking).
- **History (`/history`)**: Fetches detailed summaries of all completed sets, including logged RPE, weights, set duration, and pain flags.
- **Profile (`/profile-page`)**: Form settings for personal attributes (Age, Height, Weight, Biological Sex, and Lifestyle Factors) alongside a dedicated **Change Password** security interface.
- **Calculator (`/calculator`)**: A standalone energy estimation tool for calculating BMI, BMR, TEF, NEAT, and TDEE, with state comparison to previous metrics.

### 2. Standalone Energy Calculator
Calculates and details the following metabolic metrics:
- **BMI**: Calculated based on current height and weight.
- **BMR**: Estimated using the Mifflin-St Jeor formula.
- **TEF (Thermic Effect of Food)**: Modeled as 10% of total daily calorie expenditure.
- **NEAT (Non-Exercise Activity Thermogenesis)**: A flat `75 kcal` baseline representing incidental daily movement.
- **TDEE (Total Daily Energy Expenditure)**: BMR scaled by the selected activity multiplier (Sedentary: 1.2, Lightly Active: 1.375, Moderately Active: 1.55, Very Active: 1.725) combined with TEF and NEAT.
- *Supports relative state retention, allowing users to compare current numbers directly against their previous calculation run.*

### 3. Daily Fitness Score
Computes a dynamic fitness rating (from 1.00 to 10.00, mapped to a letter grade from A+ to F) on a daily basis:
- **82% Weight — Lifestyle Factors**: Evaluates age correctness, stress levels, sleep hygiene, and clinical BMI ranges.
- **18% Weight — Workout consistency**: Scores consistency (number of sessions in the past 7 days), webcam-tracked form performance, metabolic target calorie alignment, and recent PR set counts.
- *Supports dynamic weight redistribution if specific tracking parameters are missing, seamlessly adapting to empty states.*

### 4. AI Coach Tip
Integrates with Groq API services (`llama-3.1-8b-instant`) to fetch encouraging, custom, non-generic fitness insights based on:
- Recent workout sets, form scores, and durations.
- Current 30-day weight trends.
- Active personal records (PRs) achieved.
- Current Fitness Score and contributing sub-score breakdowns.
- *Gracefully falls back to localized tips on API key absences, rate limits, or network timeouts.*

### 5. Experimental Chronic Disease Risk Model
Accessible under the Profile page. Evaluates chronic risk probability using the trained ensemble classifier model.
- **Exploratory Disclaimer**: The model is based on synthetic dataset training where input lifestyle parameters exhibited low overall target correlation. It is explicitly labeled in the UI as an exploratory, non-diagnostic estimate, accompanied by a prominent warning block.

### 6. Admin Diagnostic Dashboard (`/admin`)
Provides administrative read-only monitoring:
- Lists all registered users, total active workout sessions logged, and timestamps of last active session dates.

### 7. Security & API Protections
- **Authentication**: Stateful sessions verified via cookie-based middleware. Registration and password changes enforce an **8-character minimum** password length constraint. Password updates require validation of the user's current password.
- **WebSocket Protection**: Gated with session checks at handshake. Rejecting unauthenticated socket requests with status `1008` (Policy Violation) protects the media execution pool from resource starvation.
- **Rate Limiting**: Integrated `slowapi` decorators intercept and throttle requests to prevent brute-force attacks:
  - `POST /api/auth/login` (Max 5 attempts / minute)
  - `POST /api/auth/register` (Max 3 attempts / minute)
  - `POST /experimental/risk-estimate` (Max 10 attempts / minute)
  - Exceeded thresholds return a formatted HTTP 429 JSON response.
- **Health Check**: A public `GET /health` route is exposed to return `{"status": "ok"}` for container health monitoring.
