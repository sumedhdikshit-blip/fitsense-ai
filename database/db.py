import sqlite3
import os
import hashlib
import secrets
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fitsense.db")

def hash_password(password: str) -> str:
    salt = secrets.token_hex(8)
    hash_val = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
    return f"{salt}${hash_val}"

def verify_password(password: str, hashed: str) -> bool:
    try:
        salt, hash_val = hashed.split('$')
        check_val = hashlib.sha256((salt + password).encode('utf-8')).hexdigest()
        return secrets.compare_digest(hash_val, check_val)
    except Exception:
        return False

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
      user_id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      username TEXT UNIQUE,
      password_hash TEXT,
      is_admin INTEGER DEFAULT 0,
      age INTEGER,
      weight_kg REAL,
      height_cm REAL,
      fitness_goal TEXT,
      sex TEXT DEFAULT 'unspecified',
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # Run migrations for user table columns if not present (for existing databases)
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN sex TEXT DEFAULT 'unspecified';")
    except sqlite3.OperationalError:
        pass # Already migrated

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN username TEXT;")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT;")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0;")
    except sqlite3.OperationalError:
        pass
        
    # 2. sessions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
      session_id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER DEFAULT 1,
      date TEXT NOT NULL,
      start_time TIMESTAMP,
      end_time TIMESTAMP,
      total_duration_mins REAL,
      total_sets INTEGER DEFAULT 0,
      total_reps INTEGER DEFAULT 0,
      avg_form_score REAL,
      total_calories_burned REAL DEFAULT 0.0,
      notes TEXT,
      FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)
    
    # 3. exercises
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercises (
      exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
      session_id INTEGER NOT NULL,
      exercise_key TEXT NOT NULL,
      exercise_name TEXT NOT NULL,
      total_sets INTEGER DEFAULT 0,
      total_reps INTEGER DEFAULT 0,
      avg_form_score REAL,
      calories_burned REAL DEFAULT 0.0,
      FOREIGN KEY (session_id) REFERENCES sessions(session_id)
    );
    """)
    
    # 4. sets
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sets (
      set_id INTEGER PRIMARY KEY AUTOINCREMENT,
      exercise_id INTEGER NOT NULL,
      set_number INTEGER NOT NULL,
      reps_counted INTEGER DEFAULT 0 CHECK (reps_counted >= 0),
      weight_kg REAL DEFAULT 0 CHECK (weight_kg >= 0),
      weight_mode TEXT DEFAULT 'total',
      rpe INTEGER,
      avg_form_score REAL,
      pain_flag BOOLEAN DEFAULT 0,
      pain_location TEXT,
      duration_seconds REAL DEFAULT 0.0 CHECK (duration_seconds >= 0),
      timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (exercise_id) REFERENCES exercises(exercise_id)
    );
    """)
    
    try:
        cursor.execute("ALTER TABLE sets ADD COLUMN duration_seconds REAL DEFAULT 0.0;")
    except sqlite3.OperationalError:
        pass # Already migrated

    try:
        cursor.execute("ALTER TABLE sets ADD COLUMN weight_mode TEXT DEFAULT 'total';")
    except sqlite3.OperationalError:
        pass # Already migrated

    # 5. recovery_logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recovery_logs (
      log_id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER DEFAULT 1,
      date TEXT NOT NULL,
      sleep_hours REAL,
      sleep_quality INTEGER,
      stress_level INTEGER,
      soreness_level INTEGER,
      hrv INTEGER,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)
    
    # 6. fitness_scores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fitness_scores (
      score_id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER DEFAULT 1,
      date TEXT NOT NULL,
      recovery_score REAL,
      fitness_score REAL,
      fatigue_score REAL,
      recommendation TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)
    
    # 7. daily_nutrition
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_nutrition (
      entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER DEFAULT 1,
      date TEXT NOT NULL,
      calories_consumed REAL DEFAULT 0.0,
      calories_burned_exercise REAL DEFAULT 0.0,
      calories_burned_bmr REAL DEFAULT 0.0,
      net_calories REAL DEFAULT 0.0,
      protein_g REAL DEFAULT 0.0,
      carbs_g REAL DEFAULT 0.0,
      fat_g REAL DEFAULT 0.0,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)
    
    # 8. weight_history
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weight_history (
      entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER DEFAULT 1,
      date TEXT NOT NULL,
      weight_kg REAL NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(user_id),
      UNIQUE(user_id, date) ON CONFLICT REPLACE
    );
    """)

    # 9. cardio_logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cardio_logs (
      log_id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER DEFAULT 1,
      date TEXT NOT NULL,
      activity_name TEXT NOT NULL,
      duration_mins REAL,
      calories_burned REAL NOT NULL,
      entry_method TEXT NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """)
    
    # Check if we have at least one user, insert default Athlete if none
    cursor.execute("SELECT COUNT(*) as count FROM users")
    if cursor.fetchone()["count"] == 0:
        hashed = hash_password("athlete")
        cursor.execute("""
        INSERT INTO users (name, username, password_hash, is_admin, age, weight_kg, height_cm, fitness_goal, sex)
        VALUES ('Athlete', 'athlete', ?, 1, 28, 75.0, 180.0, 'Strength and Form Improvement', 'unspecified')
        """, (hashed,))
    else:
        # Check if user_id=1 (Athlete) is missing username/password, and set defaults
        cursor.execute("SELECT * FROM users WHERE user_id = 1")
        row = cursor.fetchone()
        if row and (not row["username"] or not row["password_hash"]):
            hashed = hash_password("athlete")
            cursor.execute("""
                UPDATE users 
                SET username = 'athlete', password_hash = ?, is_admin = 1
                WHERE user_id = 1
            """, (hashed,))
        
    conn.commit()
    conn.close()

# User Management and Authentication

def create_user(username, password, name, age=28, weight=75.0, height=180.0, sex='unspecified', fitness_goal='Strength and Form Improvement', is_admin=0):
    conn = get_connection()
    cursor = conn.cursor()
    hashed = hash_password(password)
    try:
        cursor.execute("""
            INSERT INTO users (username, password_hash, name, age, weight_kg, height_cm, sex, fitness_goal, is_admin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (username.lower().strip(), hashed, name, age, weight, height, sex, fitness_goal, is_admin))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        raise ValueError("Username already exists")

def authenticate_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username.lower().strip(),))
    row = cursor.fetchone()
    conn.close()
    if row and verify_password(password, row["password_hash"]):
        return dict(row)
    return None

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username.lower().strip(),))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_admin_users_summary():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            u.user_id,
            u.username,
            u.name,
            u.is_admin,
            COUNT(s.session_id) as total_sessions,
            MAX(s.date) as last_active_date
        FROM users u
        LEFT JOIN sessions s ON u.user_id = s.user_id
        GROUP BY u.user_id
        ORDER BY u.user_id ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Profile settings CRUD

def get_profile(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def save_profile(user_id, name, age, weight, height, sex, fitness_goal):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE users 
        SET name = ?, age = ?, weight_kg = ?, height_cm = ?, sex = ?, fitness_goal = ?
        WHERE user_id = ?
    """, (name, age, weight, height, sex, fitness_goal, user_id))
    
    # Log to weight history automatically
    today_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        INSERT INTO weight_history (user_id, date, weight_kg)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, date) DO UPDATE SET weight_kg = excluded.weight_kg
    """, (user_id, today_str, weight))
    
    conn.commit()
    conn.close()

# Weight logs

def get_weight_history(user_id, days=90):
    conn = get_connection()
    cursor = conn.cursor()
    if days == "all" or days is None:
        cursor.execute("""
            SELECT date, weight_kg FROM weight_history 
            WHERE user_id = ? 
            ORDER BY date ASC
        """, (user_id,))
    else:
        # Fetch entries within N days
        cursor.execute("""
            SELECT date, weight_kg FROM weight_history 
            WHERE user_id = ? AND date >= date('now', '-' || ? || ' days')
            ORDER BY date ASC
        """, (user_id, int(days)))
        
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def log_weight(user_id, date, weight_kg):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Upsert weight history
    cursor.execute("""
        INSERT INTO weight_history (user_id, date, weight_kg)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, date) DO UPDATE SET weight_kg = excluded.weight_kg
    """, (user_id, date, weight_kg))
    
    # Update profile weight to match the latest logged weight
    cursor.execute("SELECT date FROM weight_history WHERE user_id = ? ORDER BY date DESC LIMIT 1", (user_id,))
    latest_date_row = cursor.fetchone()
    if latest_date_row and latest_date_row["date"] == date:
        cursor.execute("UPDATE users SET weight_kg = ? WHERE user_id = ?", (weight_kg, user_id))
        
    conn.commit()
    conn.close()

# Cardio logs

def log_cardio(user_id, date, activity_name, duration_mins, calories_burned, entry_method):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cardio_logs (user_id, date, activity_name, duration_mins, calories_burned, entry_method)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, date, activity_name, duration_mins, calories_burned, entry_method))
    conn.commit()
    conn.close()

def get_cardio_logs(user_id, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM cardio_logs 
        WHERE user_id = ? AND date = ?
        ORDER BY log_id ASC
    """, (user_id, date))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# Nutrition logs

def log_nutrition(user_id, date, calories_consumed, protein, carbs, fat):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if entry exists for this user and date
    cursor.execute("SELECT entry_id FROM daily_nutrition WHERE user_id = ? AND date = ?", (user_id, date))
    row = cursor.fetchone()
    
    if row:
        cursor.execute("""
            UPDATE daily_nutrition
            SET calories_consumed = ?, protein_g = ?, carbs_g = ?, fat_g = ?
            WHERE entry_id = ?
        """, (calories_consumed, protein, carbs, fat, row["entry_id"]))
    else:
        cursor.execute("""
            INSERT INTO daily_nutrition (user_id, date, calories_consumed, protein_g, carbs_g, fat_g)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, date, calories_consumed, protein, carbs, fat))
        
    conn.commit()
    conn.close()

def get_nutrition_data(user_id, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM daily_nutrition WHERE user_id = ? AND date = ?", (user_id, date))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# Workout sessions

def get_recent_sessions(user_id, limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            s.session_id, 
            s.date, 
            s.total_sets, 
            s.total_reps, 
            s.avg_form_score,
            s.total_calories_burned,
            (SELECT GROUP_CONCAT(exercise_name, ', ') FROM exercises WHERE session_id = s.session_id) as exercises_done
        FROM sessions s
        WHERE s.user_id = ?
        ORDER BY s.session_id DESC
        LIMIT ?
    """, (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_session_details(session_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions WHERE session_id = ? AND user_id = ?", (session_id, user_id))
    session = cursor.fetchone()
    if not session:
        conn.close()
        return None
    
    cursor.execute("SELECT * FROM exercises WHERE session_id = ?", (session_id,))
    exercises = [dict(e) for e in cursor.fetchall()]
    
    for exercise in exercises:
        cursor.execute("SELECT * FROM sets WHERE exercise_id = ? ORDER BY set_number ASC", (exercise["exercise_id"],))
        exercise["sets"] = [dict(s) for s in cursor.fetchall()]
        
    conn.close()
    
    result = dict(session)
    result["exercises"] = exercises
    return result

def create_in_progress_session(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().isoformat()
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    cursor.execute("""
        INSERT INTO sessions (user_id, date, start_time, end_time, total_duration_mins, total_sets, total_reps, avg_form_score, total_calories_burned, notes)
        VALUES (?, ?, ?, NULL, 0.0, 0, 0, 0.0, 0.0, '')
    """, (user_id, today_str, now_str))
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id

def get_or_create_exercise(session_id, exercise_key, display_name):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT exercise_id FROM exercises 
        WHERE session_id = ? AND exercise_key = ?
    """, (session_id, exercise_key))
    row = cursor.fetchone()
    
    if row:
        exercise_id = row["exercise_id"]
    else:
        cursor.execute("""
            INSERT INTO exercises (session_id, exercise_key, exercise_name, total_sets, total_reps, avg_form_score, calories_burned)
            VALUES (?, ?, ?, 0, 0, 0.0, 0.0)
        """, (session_id, exercise_key, display_name))
        exercise_id = cursor.lastrowid
        conn.commit()
        
    conn.close()
    return exercise_id

def log_set_to_db(exercise_id, set_number, reps, weight, rpe, form_score, pain_flag, pain_location, duration_seconds=0.0, weight_mode='total'):
    conn = get_connection()
    try:
        with conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO sets (exercise_id, set_number, reps_counted, weight_kg, weight_mode, rpe, avg_form_score, pain_flag, pain_location, duration_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (exercise_id, set_number, reps, weight, weight_mode, rpe, form_score, pain_flag, pain_location, duration_seconds))
            
            # Update exercise summary stats
            cursor.execute("SELECT reps_counted, avg_form_score FROM sets WHERE exercise_id = ?", (exercise_id,))
            all_sets = cursor.fetchall()
            total_reps = sum(s["reps_counted"] for s in all_sets)
            total_sets = len(all_sets)
            avg_score = sum(s["avg_form_score"] for s in all_sets) / total_sets if total_sets > 0 else 0.0
            
            cursor.execute("""
                UPDATE exercises 
                SET total_sets = ?, total_reps = ?, avg_form_score = ?
                WHERE exercise_id = ?
            """, (total_sets, total_reps, avg_score, exercise_id))
            
            # Get session_id from exercise
            cursor.execute("SELECT session_id FROM exercises WHERE exercise_id = ?", (exercise_id,))
            session_id = cursor.fetchone()["session_id"]
            
            # Update session summary stats
            cursor.execute("SELECT exercise_id FROM exercises WHERE session_id = ?", (session_id,))
            ex_ids = [e["exercise_id"] for e in cursor.fetchall()]
            
            all_session_sets = []
            for ex_id in ex_ids:
                cursor.execute("SELECT reps_counted, avg_form_score FROM sets WHERE exercise_id = ?", (ex_id,))
                all_session_sets.extend(cursor.fetchall())
                
            sess_reps = sum(s["reps_counted"] for s in all_session_sets)
            sess_sets = len(all_session_sets)
            sess_avg_score = sum(s["avg_form_score"] for s in all_session_sets) / sess_sets if sess_sets > 0 else 0.0
            
            cursor.execute("""
                UPDATE sessions 
                SET total_sets = ?, total_reps = ?, avg_form_score = ?
                WHERE session_id = ?
            """, (sess_sets, sess_reps, sess_avg_score, session_id))
    finally:
        conn.close()

def finalize_session(session_id, notes=""):
    conn = get_connection()
    try:
        with conn:
            cursor = conn.cursor()
            
            # 1. Fetch user associated with this session to query weight
            cursor.execute("SELECT user_id FROM sessions WHERE session_id = ?", (session_id,))
            sess_row = cursor.fetchone()
            user_id = sess_row["user_id"] if sess_row else 1
            
            cursor.execute("SELECT weight_kg FROM users WHERE user_id = ?", (user_id,))
            user_row = cursor.fetchone()
            weight = user_row["weight_kg"] if user_row else 75.0
            
            # 2. Get all exercises for this session
            cursor.execute("SELECT exercise_id, exercise_key FROM exercises WHERE session_id = ?", (session_id,))
            exercises = cursor.fetchall()
            
            total_session_calories = 0.0
            
            for ex in exercises:
                ex_id = ex["exercise_id"]
                ex_key = ex["exercise_key"]
                
                # Get MET value
                from config.exercise_library import EXERCISE_LIBRARY
                met = EXERCISE_LIBRARY.get(ex_key, {}).get("met_value", 3.0)
                
                # Get total duration of all sets for this exercise
                cursor.execute("SELECT SUM(duration_seconds) as total_dur FROM sets WHERE exercise_id = ?", (ex_id,))
                dur_row = cursor.fetchone()
                total_dur_seconds = dur_row["total_dur"] if (dur_row and dur_row["total_dur"]) else 0.0
                
                # Calculate calories for this exercise (MET * weight * hours)
                ex_calories = met * weight * (total_dur_seconds / 3600.0)
                total_session_calories += ex_calories
                
                # Update exercise calories
                cursor.execute("UPDATE exercises SET calories_burned = ? WHERE exercise_id = ?", (ex_calories, ex_id))
                
            # 3. Finalize session with end_time, duration, and total_calories_burned
            cursor.execute("SELECT start_time FROM sessions WHERE session_id = ?", (session_id,))
            row = cursor.fetchone()
            if not row:
                return None
            
            start_time_str = row["start_time"]
            start_time = datetime.fromisoformat(start_time_str)
            end_time = datetime.now()
            duration_mins = max(0.1, (end_time - start_time).total_seconds() / 60.0)
            
            cursor.execute("""
                UPDATE sessions 
                SET end_time = ?, total_duration_mins = ?, total_calories_burned = ?, notes = ?
                WHERE session_id = ?
            """, (end_time.isoformat(), duration_mins, total_session_calories, notes, session_id))
            
            # Retrieve updated session
            cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
            final_session = dict(cursor.fetchone())
            return final_session
    finally:
        conn.close()
