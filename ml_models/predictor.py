# FitSense AI — ML Model Predictor & Risk Estimator

import os
import joblib
import numpy as np

# ── Load model & scaler at startup ──────────────────────────────────────────
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, "chronic_disease_ensemble_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")

if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
    raise FileNotFoundError("Machine Learning model weights or scaler not found in ml_models/ directory.")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

def predict_risk(features_dict: dict) -> dict:
    """
    Accepts raw feature dictionary and returns prediction probability and class.
    
    Expected features_dict keys:
    - age: int
    - height_cm: float
    - weight_kg: float
    - bmi: float (optional, will be calculated from height/weight if missing)
    - stress_level: int (1-10)
    - sleep_hours: float
    - smoker: str ('yes' or 'no')
    - exercise_freq: str ('none', '1-2 times/week', '3-5 times/week', 'daily')
    - alcohol_consumption: str ('none', 'low', 'moderate', 'high')
    - gender: str ('female', 'male', 'other')
    - diet_quality: str ('poor', 'average', 'good', 'excellent')
    """
    # 1. Input Parsing & Case Normalization
    age = int(features_dict.get("age", 30))
    height_cm_val = features_dict.get("height_cm")
    height_cm = float(height_cm_val) if height_cm_val is not None else 0.0
    weight_kg_val = features_dict.get("weight_kg")
    weight_kg = float(weight_kg_val) if weight_kg_val is not None else 0.0
    
    # Calculate BMI if missing or invalid
    bmi_val = features_dict.get("bmi")
    bmi = float(bmi_val) if bmi_val is not None else None
    
    if bmi is None or bmi <= 0.0:
        if height_cm <= 0.0:
            bmi = None
        else:
            height_m = height_cm / 100.0
            if height_m <= 0.0:
                bmi = None
            else:
                bmi = weight_kg / (height_m ** 2)
    
    stress_level = int(features_dict.get("stress_level", 5))
    sleep_hours = float(features_dict.get("sleep_hours", 7.0))
    
    smoker_str = str(features_dict.get("smoker", "no")).strip().lower()
    smoker_val = 1 if smoker_str == "yes" else 0
    
    exercise_freq = str(features_dict.get("exercise_freq", "none")).strip().lower()
    alcohol_consumption = str(features_dict.get("alcohol_consumption", "none")).strip().lower()
    gender = str(features_dict.get("gender", "other")).strip().lower()
    diet_quality = str(features_dict.get("diet_quality", "average")).strip().lower()

    # 2. Categorical mappings matching Colab Pipeline
    exercise_map = {
        'none': 0,
        '1-2 times/week': 1,
        '3-5 times/week': 2,
        'daily': 3
    }
    alcohol_map = {
        'none': 0,
        'low': 1,
        'moderate': 2,
        'high': 3
    }
    gender_map = {
        'female': 0,
        'male': 1,
        'other': 2
    }
    diet_map = {
        'average': 0,
        'excellent': 1,
        'good': 2,
        'poor': 3
    }

    exercise_score = exercise_map.get(exercise_freq, 0)
    alcohol_score = alcohol_map.get(alcohol_consumption, 0)
    gender_score = gender_map.get(gender, 2)
    diet_score = diet_map.get(diet_quality, 0)

    # 3. Feature Engineering formulas matching Block 7, 8, 9
    smoker_norm = float(smoker_val)
    exercise_norm = float(1.0 - (exercise_score / 3.0))
    alcohol_norm = float(alcohol_score / 3.0)
    
    # sleep_hours clipped to valid [2.5, 12] range used during training
    sleep_hours_clipped = np.clip(sleep_hours, 2.5, 12.0)
    sleep_norm = float(1.0 - ((sleep_hours_clipped - 2.5) / (12.0 - 2.5)))

    # risk_score calculation
    risk_score = (
        0.4 * smoker_norm +
        0.3 * exercise_norm +
        0.2 * alcohol_norm +
        0.1 * sleep_norm
    )

    # bmi_penalty calculation
    if bmi is None:
        bmi_pen = 0.0
    elif 18.5 <= bmi <= 24.9:
        bmi_pen = 0.0
    elif bmi < 18.5:
        bmi_pen = (18.5 - bmi) / 18.5
    else:
        bmi_pen = (bmi - 24.9) / 24.9
    bmi_penalty_val = float(np.clip(bmi_pen, 0.0, 1.0))

    # stress_norm calculation
    stress_level_clipped = np.clip(stress_level, 1, 10)
    stress_norm = float((stress_level_clipped - 1) / 9.0)

    # health_rating calculation
    health_rating = 100.0 * (1.0 - (
        0.30 * smoker_norm +
        0.25 * exercise_norm +
        0.15 * alcohol_norm +
        0.10 * sleep_norm +
        0.10 * bmi_penalty_val +
        0.10 * stress_norm
    ))
    health_rating_val = float(np.clip(health_rating, 0.0, 100.0))

    # 4. Form Feature Array in training order
    # ['age', 'gender', 'height_cm', 'weight_kg', 'bmi', 'smoker', 'diet_quality',
    #  'stress_level', 'sleep_hours', 'exercise_score', 'alcohol_score', 'risk_score', 'health_rating']
    feature_vector = [
        age,
        gender_score,
        height_cm,
        weight_kg,
        0.0 if bmi is None else bmi,
        smoker_val,
        diet_score,
        stress_level,
        sleep_hours,
        exercise_score,
        alcohol_score,
        risk_score,
        health_rating_val
    ]

    # 5. Scaling
    feature_vector_scaled = scaler.transform(np.array([feature_vector]))

    # 6. Predict Probability & Label
    # Best F1 threshold found during ensemble training is 0.10
    prob = float(model.predict_proba(feature_vector_scaled)[0][1])
    predicted_class = bool(prob >= 0.10)

    return {
        "risk_probability": prob,
        "predicted_class": predicted_class
    }
