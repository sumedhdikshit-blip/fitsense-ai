import os
import sys
import time
import sqlite3

# Add fitsense-ai workspace to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import SetLogRequest
from database.db import get_connection, log_set_to_db, init_db, get_or_create_exercise, create_in_progress_session
from pose.counter import RepCounter
from pydantic import ValidationError

# ==================== MANUAL SET ENTRY TESTS ====================

def test_manual_set_entry_validation():
    """Verify that SetLogRequest validates reps, weight, weight_mode, and duration correctly."""
    # 1. Valid payload
    payload = {
        "exercise_key": "squat",
        "set_number": 1,
        "reps_counted": 10,
        "weight_kg": 40.0,
        "weight_unit": "lbs",
        "weight_mode": "per_side",
        "rpe": 8,
        "avg_form_score": 90.0,
        "pain_flag": False,
        "pain_location": "",
        "duration_seconds": 35.5
    }
    req = SetLogRequest(**payload)
    assert req.reps_counted == 10
    assert req.weight_kg == 40.0
    assert req.weight_unit == "lbs"
    assert req.weight_mode == "per_side"
    assert req.duration_seconds == 35.5

    # 2. Missing weight_mode should default to 'total'
    payload_no_mode = payload.copy()
    payload_no_mode.pop("weight_mode")
    req_no_mode = SetLogRequest(**payload_no_mode)
    assert req_no_mode.weight_mode == "total"

    # 3. Missing duration_seconds should default to 0.0
    payload_no_dur = payload.copy()
    payload_no_dur.pop("duration_seconds")
    req_no_dur = SetLogRequest(**payload_no_dur)
    assert req_no_dur.duration_seconds == 0.0

    # 4. Negative weight should fail validation
    payload_neg_weight = payload.copy()
    payload_neg_weight["weight_kg"] = -5.0
    try:
        SetLogRequest(**payload_neg_weight)
        assert False, "Expected ValidationError for negative weight"
    except ValidationError:
        pass

    # 4. Invalid RPE should fail validation
    payload_bad_rpe = payload.copy()
    payload_bad_rpe["rpe"] = 11
    try:
        SetLogRequest(**payload_bad_rpe)
        assert False, "Expected ValidationError for RPE = 11"
    except ValidationError:
        pass

def test_manual_set_db_storage():
    """Verify that manual set logs are stored in the database correctly without silent conversions."""
    init_db()
    session_id = create_in_progress_session(1)
    exercise_id = get_or_create_exercise(session_id, "pushup", "Pushup")

    # 1. Log set 1: per_side weight mode, custom duration, unit lbs
    log_set_to_db(
        exercise_id=exercise_id,
        set_number=1,
        reps=8,
        weight=25.0,
        rpe=7,
        form_score=92.0,
        pain_flag=False,
        pain_location="",
        duration_seconds=42.0,
        weight_mode="per_side",
        weight_unit="lbs"
    )

    # 2. Log set 2: total weight mode, blank duration (default 0.0), unit kg
    log_set_to_db(
        exercise_id=exercise_id,
        set_number=2,
        reps=10,
        weight=60.0,
        rpe=9,
        form_score=88.0,
        pain_flag=True,
        pain_location="right shoulder",
        duration_seconds=0.0,
        weight_mode="total",
        weight_unit="kg"
    )

    # Query the database directly to verify
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sets WHERE exercise_id = ? ORDER BY set_number ASC", (exercise_id,))
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()

    assert len(rows) == 2
    
    # Set 1 verification
    assert rows[0]["set_number"] == 1
    assert rows[0]["reps_counted"] == 8
    assert rows[0]["weight_kg"] == 25.0
    assert rows[0]["weight_unit"] == "lbs"
    assert rows[0]["weight_mode"] == "per_side"  # Saved exactly as logged
    assert rows[0]["duration_seconds"] == 42.0

    # Set 2 verification
    assert rows[1]["set_number"] == 2
    assert rows[1]["reps_counted"] == 10
    assert rows[1]["weight_kg"] == 60.0
    assert rows[1]["weight_unit"] == "kg"
    assert rows[1]["weight_mode"] == "total"  # Saved exactly as logged
    assert rows[1]["duration_seconds"] == 0.0


# ==================== TRACKING LOSS & RECONNECT TESTS ====================

def test_tracking_loss_pause_resume():
    """Verify that pose tracking loss pauses time accumulation and resumes gracefully without anomalies."""
    config = {
        "primary_angle": "left_elbow",
        "down_threshold": 90,
        "up_threshold": 160,
        "mode": "hold",
        "angles": {"left_elbow": ["left_shoulder", "left_elbow", "left_wrist"]},
        "form_rules": []
    }
    
    counter = RepCounter("plank_hold", config)
    
    # Frame 1: Valid angle within hold range. Stage -> "holding"
    counter.update({"left_elbow": 120}, {})
    assert counter.stage == "holding"
    assert counter.last_update_time is not None
    time.sleep(0.1)
    
    # Frame 2: Still holding. Good form time should accumulate.
    counter.update({"left_elbow": 120}, {})
    assert counter.good_form_time > 0.0
    last_val = counter.good_form_time
    
    # Frame 3: Tracking lost! update() is called with empty values.
    # self.last_update_time must be set to None.
    counter.update({}, {})
    assert counter.last_update_time is None
    
    # Simulate a 1-second gap of tracking loss
    time.sleep(1.0)
    
    # Frame 4: Tracking returns. First frame after tracking returns should not accumulate the 1-second gap!
    counter.update({"left_elbow": 120}, {})
    assert counter.last_update_time is not None
    # Good form time should not have accumulated the 1-second gap (it should remain very close to the last_val)
    assert counter.good_form_time - last_val < 0.2, f"Time accumulated during tracking loss: {counter.good_form_time - last_val}s"

def test_reconnect_restore_count():
    """Verify that a new WebSocket connection can restore reps_counted and continue tracking reps."""
    config = {
        "primary_angle": "left_elbow",
        "down_threshold": 150,  # Case B: bicep curl (down is larger, up is smaller)
        "up_threshold": 40,
        "mode": "rep",
        "angles": {"left_elbow": ["left_shoulder", "left_elbow", "left_wrist"]},
        "form_rules": []
    }
    
    # Simulate reconnect by starting counter and restoring reps_counted to 5
    counter = RepCounter("bicep_curl", config)
    counter.reps_counted = 5  # Restored count
    
    # Run a valid rep flow:
    # First frame to initialize: angle is 160 (down)
    counter.update({"left_elbow": 160}, {})
    assert counter.stage == "down"
    assert counter.reps_counted == 5
    
    # Flex elbow to 35 (below up_threshold 40)
    counter.update({"left_elbow": 35}, {})
    assert counter.stage == "up"
    # Count should increment to 6
    assert counter.reps_counted == 6

def test_db_check_constraints():
    """Verify that sets table check constraints prevent negative reps, weight, or duration."""
    import tempfile
    
    # Create a temporary DB file
    temp_db_fd, temp_db_path = tempfile.mkstemp()
    os.close(temp_db_fd)
    
    try:
        # Override DB_PATH in database.db module temporarily
        from database import db
        original_db_path = db.DB_PATH
        db.DB_PATH = temp_db_path
        
        # Initialize the database with schema containing the CHECK constraints
        db.init_db()
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Insert a dummy session and exercise
        cursor.execute("INSERT INTO sessions (date, start_time) VALUES ('2026-07-05', '2026-07-05T09:00:00')")
        session_id = cursor.lastrowid
        cursor.execute("INSERT INTO exercises (session_id, exercise_key, exercise_name) VALUES (?, 'pushup', 'Pushup')", (session_id,))
        exercise_id = cursor.lastrowid
        conn.commit()
        
        # 1. Test negative reps_counted should fail
        try:
            cursor.execute("INSERT INTO sets (exercise_id, set_number, reps_counted, weight_kg, duration_seconds) VALUES (?, 1, -5, 10.0, 30.0)", (exercise_id,))
            conn.commit()
            assert False, "Expected sqlite3.IntegrityError for negative reps"
        except sqlite3.IntegrityError:
            pass # Correctly failed
            
        # 2. Test negative weight should fail
        try:
            cursor.execute("INSERT INTO sets (exercise_id, set_number, reps_counted, weight_kg, duration_seconds) VALUES (?, 1, 10, -10.0, 30.0)", (exercise_id,))
            conn.commit()
            assert False, "Expected sqlite3.IntegrityError for negative weight"
        except sqlite3.IntegrityError:
            pass # Correctly failed

        # 3. Test negative duration should fail
        try:
            cursor.execute("INSERT INTO sets (exercise_id, set_number, reps_counted, weight_kg, duration_seconds) VALUES (?, 1, 10, 10.0, -30.0)", (exercise_id,))
            conn.commit()
            assert False, "Expected sqlite3.IntegrityError for negative duration"
        except sqlite3.IntegrityError:
            pass # Correctly failed

        try:
            conn.close()
        except:
            pass
    finally:
        # Restore DB_PATH and cleanup temp file
        from database import db
        db.DB_PATH = original_db_path
        try:
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        except PermissionError:
            pass

def test_password_hashing_helpers():
    """Verify that hash_password creates secure unique hashes and verify_password validates correctly."""
    from database import db
    pwd = "secret_password"
    hashed1 = db.hash_password(pwd)
    hashed2 = db.hash_password(pwd)
    
    # Hashes must use random salts, so they must be different
    assert hashed1 != hashed2
    
    # Verification should succeed with correct password
    assert db.verify_password(pwd, hashed1)
    assert db.verify_password(pwd, hashed2)
    
    # Verification should fail with incorrect password
    assert not db.verify_password("wrong_password", hashed1)

def test_user_registration_and_authentication():
    """Verify user registration, duplicate username rejection, and credential authentication."""
    import tempfile
    from database import db
    
    temp_db_fd, temp_db_path = tempfile.mkstemp()
    os.close(temp_db_fd)
    
    try:
        original_db_path = db.DB_PATH
        db.DB_PATH = temp_db_path
        db.init_db()
        
        # 1. Create a new user
        uid1 = db.create_user("user_a", "pass_a", "User Alpha")
        assert uid1 is not None
        assert uid1 > 1 # athlete has user_id = 1
        
        # 2. Test duplicate username raises ValueError
        try:
            db.create_user("user_a", "pass_different", "User Duplicate")
            assert False, "Expected ValueError for duplicate username"
        except ValueError:
            pass
            
        # 3. Authenticate with correct credentials
        user = db.authenticate_user("user_a", "pass_a")
        assert user is not None
        assert user["user_id"] == uid1
        assert user["name"] == "User Alpha"
        assert user["username"] == "user_a"
        
        # 4. Authenticate with incorrect credentials
        assert db.authenticate_user("user_a", "wrong_password") is None
        assert db.authenticate_user("non_existent", "pass_a") is None
        
    finally:
        db.DB_PATH = original_db_path
        try:
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        except PermissionError:
            pass

def test_multi_user_data_isolation():
    """Verify that user sessions and logs are fully isolated and User A cannot query User B's sessions."""
    import tempfile
    from database import db
    
    temp_db_fd, temp_db_path = tempfile.mkstemp()
    os.close(temp_db_fd)
    
    try:
        original_db_path = db.DB_PATH
        db.DB_PATH = temp_db_path
        db.init_db()
        
        uid1 = db.create_user("user_1", "pass", "User One")
        uid2 = db.create_user("user_2", "pass", "User Two")
        
        # Log session for user 1
        sess1 = db.create_in_progress_session(uid1)
        # Log session for user 2
        sess2 = db.create_in_progress_session(uid2)
        
        # Verify get_recent_sessions splits them correctly
        user1_sessions = db.get_recent_sessions(uid1)
        user2_sessions = db.get_recent_sessions(uid2)
        
        assert len(user1_sessions) == 1
        assert user1_sessions[0]["session_id"] == sess1
        assert len(user2_sessions) == 1
        assert user2_sessions[0]["session_id"] == sess2
        
        # Verify get_session_details prevents cross-user access
        assert db.get_session_details(sess1, uid1) is not None
        assert db.get_session_details(sess1, uid2) is None # Blocks access!
        assert db.get_session_details(sess2, uid2) is not None
        assert db.get_session_details(sess2, uid1) is None # Blocks access!
        
    finally:
        db.DB_PATH = original_db_path
        try:
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        except PermissionError:
            pass

def test_food_search_and_logging():
    """Verify that food searching and logging endpoints function correctly and accumulate properly."""
    import tempfile
    from database import db
    from fastapi.testclient import TestClient
    from main import app
    
    temp_db_fd, temp_db_path = tempfile.mkstemp()
    os.close(temp_db_fd)
    
    try:
        original_db_path = db.DB_PATH
        db.DB_PATH = temp_db_path
        db.init_db()
        
        # Seed a test food item
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO food_database (
                name, serving_description, calories, protein_g, carbs_g, fat_g,
                saturated_fat_g, fiber_g, sodium_mg, sugar_g, calcium_mg, iron_mg, vitamin_c_mg
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "Test Apple", "100g", 52.0, 0.3, 13.8, 0.2, 0.0, 2.4, 1.0, 10.4, 6.0, 0.1, 4.6
        ))
        conn.commit()
        conn.close()
        
        client = TestClient(app)
        
        # Mock auth via dependency override
        from main import get_current_user_id
        app.dependency_overrides[get_current_user_id] = lambda: 1
        
        # 1. Search for Apple
        resp = client.get("/food/search?q=Apple")
        assert resp.status_code == 200
        results = resp.json()
        assert len(results) >= 1
        assert results[0]["name"] == "Test Apple"
        assert results[0]["calories"] == 52.0
        
        # 2. Log food (1.5 servings = 150g)
        log_payload = {
            "date": "2026-07-07",
            "calories_consumed": 78.0,
            "protein_g": 0.45,
            "carbs_g": 20.7,
            "fat_g": 0.3,
            "saturated_fat_g": 0.0,
            "fiber_g": 3.6,
            "sodium_mg": 1.5,
            "sugar_g": 15.6,
            "calcium_mg": 9.0,
            "iron_mg": 0.15,
            "vitamin_c_mg": 6.9
        }
        resp = client.post("/nutrition/log", json=log_payload)
        assert resp.status_code == 200
        
        # 3. Retrieve nutrition data and assert scaled totals match
        nutrition_data = db.get_nutrition_data(1, "2026-07-07")
        assert nutrition_data is not None
        assert nutrition_data["calories_consumed"] == 78.0
        assert nutrition_data["protein_g"] == 0.45
        assert nutrition_data["carbs_g"] == 20.7
        assert nutrition_data["fat_g"] == 0.3
        assert nutrition_data["fiber_g"] == 3.6
        assert nutrition_data["sodium_mg"] == 1.5
        assert nutrition_data["sugar_g"] == 15.6
        assert nutrition_data["calcium_mg"] == 9.0
        assert nutrition_data["iron_mg"] == 0.15
        assert nutrition_data["vitamin_c_mg"] == 6.9
        
        # 4. Log manual entry fallback (accumulates)
        manual_payload = {
            "date": "2026-07-07",
            "calories_consumed": 200.0,
            "protein_g": 10.0,
            "carbs_g": 20.0,
            "fat_g": 5.0,
            "saturated_fat_g": 0.0,
            "fiber_g": 0.0,
            "sodium_mg": 0.0,
            "sugar_g": 0.0,
            "calcium_mg": 0.0,
            "iron_mg": 0.0,
            "vitamin_c_mg": 0.0
        }
        resp = client.post("/nutrition/log", json=manual_payload)
        assert resp.status_code == 200
        
        # Verify accumulation
        nutrition_data2 = db.get_nutrition_data(1, "2026-07-07")
        assert nutrition_data2["calories_consumed"] == 278.0
        assert nutrition_data2["protein_g"] == 10.45
        assert nutrition_data2["carbs_g"] == 40.7
        assert nutrition_data2["fat_g"] == 5.3
        
        # Clean dependency overrides
        app.dependency_overrides.clear()
        
    finally:
        db.DB_PATH = original_db_path
        try:
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        except PermissionError:
            pass

def test_nutrition_alerts():
    """Verify that daily nutrition alerts for low fiber, low protein, and high saturated fat compute correctly."""
    import tempfile
    from database import db
    from fastapi.testclient import TestClient
    from main import app
    
    temp_db_fd, temp_db_path = tempfile.mkstemp()
    os.close(temp_db_fd)
    
    try:
        original_db_path = db.DB_PATH
        db.DB_PATH = temp_db_path
        db.init_db()
        
        # 1. Test case with full profile details (75.0 kg, Moderately active -> 1.2 g/kg multiplier)
        # Seed user profile
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users 
            SET weight_kg = 75.0, exercise_freq = '3-5 times/week' 
            WHERE user_id = 1
        """)
        conn.commit()
        conn.close()
        
        client = TestClient(app)
        
        # Mock auth via dependency override
        from main import get_current_user_id
        app.dependency_overrides[get_current_user_id] = lambda: 1
        
        # Log food entry producing:
        # - Low fiber: 10.0g (< 20g)
        # - Low protein: 45.0g (< target 90.0g)
        # - High saturated fat: 30.0g (> 25g)
        log_payload = {
            "date": "2026-07-07",
            "calories_consumed": 1500.0,
            "protein_g": 45.0,
            "carbs_g": 150.0,
            "fat_g": 60.0,
            "saturated_fat_g": 30.0,
            "fiber_g": 10.0,
            "sodium_mg": 1000.0,
            "sugar_g": 40.0,
            "calcium_mg": 300.0,
            "iron_mg": 10.0,
            "vitamin_c_mg": 50.0
        }
        resp = client.post("/nutrition/log", json=log_payload)
        assert resp.status_code == 200
        
        # Request alerts
        resp = client.get("/nutrition/alerts?date=2026-07-07")
        assert resp.status_code == 200
        alerts = resp.json()
        
        # Expecting all 3 alerts
        assert len(alerts) == 3
        alert_types = [a["type"] for a in alerts]
        assert "fiber" in alert_types
        assert "protein" in alert_types
        assert "saturated_fat" in alert_types
        
        # Fiber message verification
        fiber_alert = next(a for a in alerts if a["type"] == "fiber")
        assert "Fiber intake is low today (10.0g of a general 20g+ guideline)" in fiber_alert["message"]
        
        # Protein message verification (target = 75.0 * 1.2 = 90.0g)
        protein_alert = next(a for a in alerts if a["type"] == "protein")
        assert "Protein intake is 45.0g, below your target of 90.0g for your activity level (1.2 g/kg" in protein_alert["message"]
        
        # Saturated fat message verification
        sat_alert = next(a for a in alerts if a["type"] == "saturated_fat")
        assert "Saturated fat intake is 30.0g today, above the general 25g guideline." in sat_alert["message"]
        
        # 2. Test graceful handling when profile details are missing
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET exercise_freq = NULL, weight_kg = NULL WHERE user_id = 1")
        conn.commit()
        conn.close()
        
        resp = client.get("/nutrition/alerts?date=2026-07-07")
        assert resp.status_code == 200
        alerts2 = resp.json()
        
        # Expecting only 2 alerts now (fiber and saturated fat), protein alert skipped gracefully
        assert len(alerts2) == 2
        alert_types2 = [a["type"] for a in alerts2]
        assert "fiber" in alert_types2
        assert "saturated_fat" in alert_types2
        assert "protein" not in alert_types2
        
        app.dependency_overrides.clear()
        
    finally:
        db.DB_PATH = original_db_path
        try:
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        except PermissionError:
            pass

def test_nutrition_history():
    """Verify that daily nutrition history query returns structured values correctly."""
    import tempfile
    from database import db
    from fastapi.testclient import TestClient
    from main import app
    
    temp_db_fd, temp_db_path = tempfile.mkstemp()
    os.close(temp_db_fd)
    
    try:
        original_db_path = db.DB_PATH
        db.DB_PATH = temp_db_path
        db.init_db()
        
        client = TestClient(app)
        from main import get_current_user_id
        app.dependency_overrides[get_current_user_id] = lambda: 1
        
        # Log food entries on today's date
        log_payload = {
            "date": "2026-07-07",
            "calories_consumed": 1500.0,
            "protein_g": 45.0,
            "carbs_g": 150.0,
            "fat_g": 60.0,
            "saturated_fat_g": 10.0,
            "fiber_g": 22.0,
            "sodium_mg": 1000.0,
            "sugar_g": 40.0,
            "calcium_mg": 300.0,
            "iron_mg": 10.0,
            "vitamin_c_mg": 50.0
        }
        resp = client.post("/nutrition/log", json=log_payload)
        assert resp.status_code == 200
        
        # Fetch 7-day history
        resp = client.get("/nutrition/history?days=7")
        assert resp.status_code == 200
        history = resp.json()
        
        assert len(history) >= 1
        day_entry = history[0]
        assert day_entry["date"] == "2026-07-07"
        assert day_entry["calories_consumed"] == 1500.0
        assert day_entry["protein_g"] == 45.0
        assert day_entry["carbs_g"] == 150.0
        assert day_entry["fat_g"] == 60.0
        assert day_entry["fiber_g"] == 22.0
        assert day_entry["saturated_fat_g"] == 10.0
        
        app.dependency_overrides.clear()
        
    finally:
        db.DB_PATH = original_db_path
        try:
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        except PermissionError:
            pass

def test_weight_goal_management():
    """Verify weight goal saving, retrieval, and profile logic."""
    import tempfile
    from database import db
    from fastapi.testclient import TestClient
    from main import app
    
    temp_db_fd, temp_db_path = tempfile.mkstemp()
    os.close(temp_db_fd)
    
    try:
        original_db_path = db.DB_PATH
        db.DB_PATH = temp_db_path
        db.init_db()
        
        client = TestClient(app)
        from main import get_current_user_id
        app.dependency_overrides[get_current_user_id] = lambda: 1
        
        # Save weight goal via endpoint
        payload = {
            "goal_type": "lose",
            "target_weight_kg": 75.5,
            "starting_weight_kg": 85.0,
            "target_date": "2026-12-31"
        }
        resp = client.post("/profile/weight-goal", json=payload)
        assert resp.status_code == 200
        
        # Verify stored in user profile
        profile = db.get_profile(1)
        assert profile["goal_type"] == "lose"
        assert profile["target_weight_kg"] == 75.5
        assert profile["starting_weight_kg"] == 85.0
        assert profile["target_date"] == "2026-12-31"
        
        app.dependency_overrides.clear()
        
    finally:
        db.DB_PATH = original_db_path
        try:
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        except PermissionError:
            pass


