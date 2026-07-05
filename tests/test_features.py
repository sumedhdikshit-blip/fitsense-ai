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
    session_id = create_in_progress_session()
    exercise_id = get_or_create_exercise(session_id, "pushup", "Pushup")

    # 1. Log set 1: per_side weight mode, custom duration
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
        weight_mode="per_side"
    )

    # 2. Log set 2: total weight mode, blank duration (default 0.0)
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
        weight_mode="total"
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
    assert rows[0]["weight_mode"] == "per_side"  # Saved exactly as logged
    assert rows[0]["duration_seconds"] == 42.0

    # Set 2 verification
    assert rows[1]["set_number"] == 2
    assert rows[1]["reps_counted"] == 10
    assert rows[1]["weight_kg"] == 60.0
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

        conn.close()
    finally:
        # Restore DB_PATH and cleanup temp file
        from database import db
        db.DB_PATH = original_db_path
        if os.path.exists(temp_db_path):
            os.remove(temp_db_path)
