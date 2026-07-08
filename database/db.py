import sqlite3
import os
import hashlib
import secrets
from datetime import datetime
import json

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
      gender TEXT,
      diet_quality TEXT,
      stress_level INTEGER,
      sleep_hours REAL,
      smoker TEXT,
      exercise_freq TEXT,
      alcohol_consumption TEXT,
      goal_type TEXT,
      target_weight_kg REAL,
      starting_weight_kg REAL,
      target_date TEXT,
      pace TEXT,
      muscle_focus TEXT,
      maintenance_focus TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # Run migrations for user table columns if not present (for existing databases)
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN goal_type TEXT;")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN target_weight_kg REAL;")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN starting_weight_kg REAL;")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN target_date TEXT;")
    except sqlite3.OperationalError:
        pass

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

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN gender TEXT;")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN diet_quality TEXT;")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN stress_level INTEGER;")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN sleep_hours REAL;")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN smoker TEXT;")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN exercise_freq TEXT;")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN alcohol_consumption TEXT;")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE users ADD COLUMN pace TEXT;")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN muscle_focus TEXT;")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN maintenance_focus TEXT;")
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
      weight_unit TEXT DEFAULT 'kg',
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

    try:
        cursor.execute("ALTER TABLE sets ADD COLUMN weight_unit TEXT DEFAULT 'kg';")
    except sqlite3.OperationalError:
        pass # Already migrated

    try:
        cursor.execute("ALTER TABLE sets ADD COLUMN form_violations TEXT DEFAULT '[]';")
    except sqlite3.OperationalError:
        pass # Already migrated


    try:
        cursor.execute("ALTER TABLE daily_nutrition ADD COLUMN saturated_fat_g REAL DEFAULT 0.0;")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE daily_nutrition ADD COLUMN fiber_g REAL DEFAULT 0.0;")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE daily_nutrition ADD COLUMN sodium_mg REAL DEFAULT 0.0;")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE daily_nutrition ADD COLUMN sugar_g REAL DEFAULT 0.0;")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE daily_nutrition ADD COLUMN calcium_mg REAL DEFAULT 0.0;")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE daily_nutrition ADD COLUMN iron_mg REAL DEFAULT 0.0;")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE daily_nutrition ADD COLUMN vitamin_c_mg REAL DEFAULT 0.0;")
    except sqlite3.OperationalError:
        pass

    try:
        cursor.execute("ALTER TABLE food_database ADD COLUMN meal_category TEXT;")
    except sqlite3.OperationalError:
        pass

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
      saturated_fat_g REAL DEFAULT 0.0,
      fiber_g REAL DEFAULT 0.0,
      sodium_mg REAL DEFAULT 0.0,
      sugar_g REAL DEFAULT 0.0,
      calcium_mg REAL DEFAULT 0.0,
      iron_mg REAL DEFAULT 0.0,
      vitamin_c_mg REAL DEFAULT 0.0,
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
    
    # 10. food_database
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_database (
      food_id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      serving_description TEXT,
      calories REAL,
      protein_g REAL,
      carbs_g REAL,
      fat_g REAL,
      saturated_fat_g REAL,
      fiber_g REAL,
      sodium_mg REAL,
      sugar_g REAL,
      calcium_mg REAL,
      iron_mg REAL,
      vitamin_c_mg REAL,
      meal_category TEXT
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
    # Create indexes for performance optimization
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_user_date ON sessions(user_id, date);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_exercises_session ON exercises(session_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sets_exercise ON sets(exercise_id);")
        
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

def update_user_password(user_id, hashed_password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users 
        SET password_hash = ?
        WHERE user_id = ?
    """, (hashed_password, user_id))
    conn.commit()
    conn.close()

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
    if row:
        res = dict(row)
        res.pop("password_hash", None)
        return res
    return None

def save_profile(user_id, name, age, weight, height, sex, fitness_goal, gender=None, diet_quality=None, stress_level=None, sleep_hours=None, smoker=None, exercise_freq=None, alcohol_consumption=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE users 
        SET name = ?, age = ?, weight_kg = ?, height_cm = ?, sex = ?, fitness_goal = ?,
            gender = ?, diet_quality = ?, stress_level = ?, sleep_hours = ?, smoker = ?,
            exercise_freq = ?, alcohol_consumption = ?
        WHERE user_id = ?
    """, (name, age, weight, height, sex, fitness_goal, gender, diet_quality, stress_level, sleep_hours, smoker, exercise_freq, alcohol_consumption, user_id))
    
    # Log to weight history automatically
    today_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        INSERT INTO weight_history (user_id, date, weight_kg)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id, date) DO UPDATE SET weight_kg = excluded.weight_kg
    """, (user_id, today_str, weight))
    
    conn.commit()
    conn.close()

def save_weight_goal(user_id, goal_type, target_weight_kg, starting_weight_kg, target_date, pace=None, muscle_focus=None, maintenance_focus=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users 
        SET goal_type = ?, target_weight_kg = ?, starting_weight_kg = ?, target_date = ?,
            pace = ?, muscle_focus = ?, maintenance_focus = ?
        WHERE user_id = ?
    """, (goal_type, target_weight_kg, starting_weight_kg, target_date, pace, muscle_focus, maintenance_focus, user_id))
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
    
    # Update profile weight to match the entry with the most recent date that is NOT after today
    today_str = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT weight_kg FROM weight_history
        WHERE user_id = ? AND date <= ?
        ORDER BY date DESC LIMIT 1
    """, (user_id, today_str))
    latest_valid_row = cursor.fetchone()
    if latest_valid_row:
        cursor.execute("UPDATE users SET weight_kg = ? WHERE user_id = ?", (latest_valid_row["weight_kg"], user_id))
        
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

def log_nutrition(user_id, date, calories_consumed, protein, carbs, fat, saturated_fat=0.0, fiber=0.0, sodium=0.0, sugar=0.0, calcium=0.0, iron=0.0, vitamin_c=0.0):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if entry exists for this user and date
    cursor.execute("SELECT entry_id FROM daily_nutrition WHERE user_id = ? AND date = ?", (user_id, date))
    row = cursor.fetchone()
    
    if row:
        cursor.execute("""
            UPDATE daily_nutrition
            SET calories_consumed = calories_consumed + ?,
                protein_g = protein_g + ?,
                carbs_g = carbs_g + ?,
                fat_g = fat_g + ?,
                saturated_fat_g = saturated_fat_g + ?,
                fiber_g = fiber_g + ?,
                sodium_mg = sodium_mg + ?,
                sugar_g = sugar_g + ?,
                calcium_mg = calcium_mg + ?,
                iron_mg = iron_mg + ?,
                vitamin_c_mg = vitamin_c_mg + ?
            WHERE entry_id = ?
        """, (calories_consumed, protein, carbs, fat, saturated_fat, fiber, sodium, sugar, calcium, iron, vitamin_c, row["entry_id"]))
    else:
        cursor.execute("""
            INSERT INTO daily_nutrition (
                user_id, date, calories_consumed, protein_g, carbs_g, fat_g,
                saturated_fat_g, fiber_g, sodium_mg, sugar_g, calcium_mg, iron_mg, vitamin_c_mg
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, date, calories_consumed, protein, carbs, fat, saturated_fat, fiber, sodium, sugar, calcium, iron, vitamin_c))
        
    conn.commit()
    conn.close()

def get_nutrition_data(user_id, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM daily_nutrition WHERE user_id = ? AND date = ?", (user_id, date))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_nutrition_history(user_id, days=7):
    conn = get_connection()
    cursor = conn.cursor()
    if days == "all" or days is None:
        cursor.execute("""
            SELECT date, calories_consumed, protein_g, carbs_g, fat_g, fiber_g, saturated_fat_g 
            FROM daily_nutrition 
            WHERE user_id = ? 
            ORDER BY date ASC
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT date, calories_consumed, protein_g, carbs_g, fat_g, fiber_g, saturated_fat_g 
            FROM daily_nutrition 
            WHERE user_id = ? AND date >= date('now', '-' || ? || ' days')
            ORDER BY date ASC
        """, (user_id, int(days)))
        
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

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
            (SELECT GROUP_CONCAT(exercise_name, ?) FROM exercises WHERE session_id = s.session_id) as exercises_done
        FROM sessions s
        WHERE s.user_id = ?
        ORDER BY s.session_id DESC
        LIMIT ?
    """, (', ', user_id, limit))
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

def log_set_to_db(exercise_id, set_number, reps, weight, rpe, form_score, pain_flag, pain_location, duration_seconds=0.0, weight_mode='total', weight_unit='kg', form_violations=None):
    conn = get_connection()
    try:
        with conn:
            cursor = conn.cursor()
            
            violations_str = "[]"
            if form_violations is not None:
                violations_str = json.dumps(form_violations)
                
            cursor.execute("""
                INSERT INTO sets (exercise_id, set_number, reps_counted, weight_kg, weight_unit, weight_mode, rpe, avg_form_score, pain_flag, pain_location, duration_seconds, form_violations)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (exercise_id, set_number, reps, weight, weight_unit, weight_mode, rpe, form_score, pain_flag, pain_location, duration_seconds, violations_str))
            
            # Update exercise summary stats
            cursor.execute("SELECT reps_counted, avg_form_score FROM sets WHERE exercise_id = ?", (exercise_id,))
            all_sets = cursor.fetchall()
            total_reps = sum(s["reps_counted"] for s in all_sets)
            total_sets = len(all_sets)
            
            valid_form_sets = [s["avg_form_score"] for s in all_sets if s["avg_form_score"] > 0.0]
            avg_score = sum(valid_form_sets) / len(valid_form_sets) if valid_form_sets else 0.0
            
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
            
            valid_session_form_sets = [s["avg_form_score"] for s in all_session_sets if s["avg_form_score"] > 0.0]
            sess_avg_score = sum(valid_session_form_sets) / len(valid_session_form_sets) if valid_session_form_sets else 0.0
            
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
            try:
                start_time = datetime.fromisoformat(start_time_str)
                end_time = datetime.now()
                duration_mins = max(0.1, (end_time - start_time).total_seconds() / 60.0)
            except (ValueError, TypeError) as e:
                import logging
                logging.warning(f"Malformed start_time '{start_time_str}' in session finalization: {e}")
                end_time = datetime.now()
                duration_mins = 0.0
            
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


def get_user_prs(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    # Fetch all weight sets
    cursor.execute("""
        SELECT e.exercise_name, s.weight_kg, s.weight_unit
        FROM sets s
        JOIN exercises e ON s.exercise_id = e.exercise_id
        JOIN sessions sess ON e.session_id = sess.session_id
        WHERE sess.user_id = ? AND s.weight_kg > 0
    """, (user_id,))
    weight_rows = cursor.fetchall()
    
    # Fetch all reps sets
    cursor.execute("""
        SELECT e.exercise_name, s.reps_counted
        FROM sets s
        JOIN exercises e ON s.exercise_id = e.exercise_id
        JOIN sessions sess ON e.session_id = sess.session_id
        WHERE sess.user_id = ? AND s.reps_counted > 0
    """, (user_id,))
    reps_rows = cursor.fetchall()
    conn.close()
    
    # Group weight sets by exercise name
    by_name_weight = {}
    for row in weight_rows:
        name = row["exercise_name"]
        if name not in by_name_weight:
            by_name_weight[name] = []
        by_name_weight[name].append(row)
        
    prs = {}
    for name, sets in by_name_weight.items():
        # Compare normalized weights: 1 lb = 0.453592 kg
        best_set = max(sets, key=lambda s: s["weight_kg"] * 0.453592 if s["weight_unit"] == "lbs" else s["weight_kg"])
        unit = best_set["weight_unit"] if best_set["weight_unit"] else "kg"
        prs[name] = {"weight": f"{best_set['weight_kg']} {unit}"}
        
    # Group reps sets by exercise name
    by_name_reps = {}
    for row in reps_rows:
        name = row["exercise_name"]
        if name not in by_name_reps:
            by_name_reps[name] = []
        by_name_reps[name].append(row)
        
    for name, sets in by_name_reps.items():
        max_reps = max(s["reps_counted"] for s in sets)
        if name not in prs:
            prs[name] = {}
        prs[name]["reps"] = f"{max_reps} reps"
        
    return prs


def get_recent_prs_count(user_id, seven_days_ago_str):
    """
    Counts the number of newly achieved PRs in the last 7 days.
    
    NOTE: If a single exercise breaks both its weight PR and its reps PR, this function
    will count it as 2 separate PRs. This is acceptable and expected since the primary
    downstream consumer (the Daily Fitness Score calculation) treats this metric as binary
    (e.g., scoring 10.0 if pr_count > 0, else 0.0). No other system caller relies on
    an exact count of unique exercises with PRs.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT e.exercise_key, s.weight_kg, s.weight_unit, s.reps_counted, sess.date
        FROM sets s
        JOIN exercises e ON s.exercise_id = e.exercise_id
        JOIN sessions sess ON e.session_id = sess.session_id
        WHERE sess.user_id = ?
    """, (user_id,))
    all_sets = cursor.fetchall()
    conn.close()
    
    by_ex = {}
    for row in all_sets:
        ex_key = row["exercise_key"]
        if ex_key not in by_ex:
            by_ex[ex_key] = []
        by_ex[ex_key].append(row)
        
    new_prs = 0
    for ex_key, sets in by_ex.items():
        # Max weight check
        valid_w_sets = [s for s in sets if s["weight_kg"] > 0]
        if valid_w_sets:
            # find max normalized weight (in kg)
            max_norm = max(s["weight_kg"] * 0.453592 if s["weight_unit"] == "lbs" else s["weight_kg"] for s in valid_w_sets)
            # check if the max normalized weight was achieved in the last 7 days
            if any((s["weight_kg"] * 0.453592 if s["weight_unit"] == "lbs" else s["weight_kg"]) >= max_norm - 1e-4 and s["date"] >= seven_days_ago_str for s in valid_w_sets):
                new_prs += 1
                
        # Max reps check
        valid_r_sets = [s for s in sets if s["reps_counted"] > 0]
        if valid_r_sets:
            max_reps = max(s["reps_counted"] for s in valid_r_sets)
            if any(s["reps_counted"] == max_reps and s["date"] >= seven_days_ago_str for s in valid_r_sets):
                new_prs += 1
                
    return new_prs

def get_strength_trend_data(user_id: int, exercise_key: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.date, st.reps_counted, st.weight_kg, st.weight_unit
        FROM sets st
        JOIN exercises e ON st.exercise_id = e.exercise_id
        JOIN sessions s ON e.session_id = s.session_id
        WHERE s.user_id = ? AND e.exercise_key = ?
        ORDER BY s.date ASC
    """, (user_id, exercise_key))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_form_patterns(user_id: int):
    from datetime import datetime, timedelta
    conn = get_connection()
    cursor = conn.cursor()
    
    date_limit = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        SELECT 
            e.exercise_key,
            e.exercise_name AS display_name,
            st.set_number,
            st.avg_form_score,
            st.form_violations,
            s.date,
            e.session_id
        FROM sets st
        JOIN exercises e ON st.exercise_id = e.exercise_id
        JOIN sessions s ON e.session_id = s.session_id
        WHERE s.user_id = ? AND st.timestamp >= ?
        ORDER BY e.exercise_key, e.session_id, st.set_number
    """, (user_id, date_limit))
    rows = cursor.fetchall()
    conn.close()
    
    exercise_sets = {}
    for r in rows:
        key = r["exercise_key"]
        if key not in exercise_sets:
            exercise_sets[key] = {
                "display_name": r["display_name"],
                "sets": []
            }
        exercise_sets[key]["sets"].append(r)
        
    results = {}
    for key, data in exercise_sets.items():
        sets = data["sets"]
        display_name = data["display_name"]
        
        if len(sets) < 5:
            continue
            
        rule_counts = {}
        for s in sets:
            violations_str = s["form_violations"]
            if violations_str:
                try:
                    violations = json.loads(violations_str)
                    if isinstance(violations, list) and len(violations) > 0:
                        for v in set(violations):
                            rule_counts[v] = rule_counts.get(v, 0) + 1
                except Exception:
                    pass
                    
        most_common_rule = None
        most_common_pct = 0.0
        if rule_counts:
            sorted_rules = sorted(rule_counts.items(), key=lambda x: x[1], reverse=True)
            top_rule, count = sorted_rules[0]
            most_common_rule = top_rule
            most_common_pct = (count / len(sets)) * 100.0
            
        session_groups = {}
        for s in sets:
            sess_id = s["session_id"]
            if sess_id not in session_groups:
                session_groups[sess_id] = []
            session_groups[sess_id].append(s)
            
        total_first_half_score = 0.0
        total_first_half_count = 0
        total_second_half_score = 0.0
        total_second_half_count = 0
        
        for sess_id, s_list in session_groups.items():
            s_list.sort(key=lambda x: x["set_number"])
            n = len(s_list)
            if n < 2:
                continue
            mid = n // 2
            first_half = s_list[:mid]
            second_half = s_list[mid:]
            
            for s in first_half:
                if s["avg_form_score"] is not None:
                    total_first_half_score += s["avg_form_score"]
                    total_first_half_count += 1
            for s in second_half:
                if s["avg_form_score"] is not None:
                    total_second_half_score += s["avg_form_score"]
                    total_second_half_count += 1
                    
        fatigue_detected = False
        avg_first_half = 0.0
        avg_second_half = 0.0
        
        if total_first_half_count > 0 and total_second_half_count > 0:
            avg_first_half = total_first_half_score / total_first_half_count
            avg_second_half = total_second_half_score / total_second_half_count
            if avg_first_half - avg_second_half >= 3.0:
                fatigue_detected = True
                
        results[key] = {
            "display_name": display_name,
            "total_sets": len(sets),
            "recurring_issue": {
                "rule": most_common_rule,
                "percentage": round(most_common_pct, 1)
            } if most_common_rule else None,
            "fatigue_pattern": {
                "detected": fatigue_detected,
                "first_half_avg": round(avg_first_half, 1),
                "second_half_avg": round(avg_second_half, 1)
            } if (total_first_half_count > 0 and total_second_half_count > 0) else None
        }
        
    return results


