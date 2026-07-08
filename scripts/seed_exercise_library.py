# FitSense AI — Exercise Library Seeding Script

import os
import sqlite3
import json
import urllib.request

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fitsense.db")
JSON_URL = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json"

def seed_database():
    print("Connecting to database...")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # 1. Create table if not exists (in case it wasn't run via init_db)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exercise_library (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT UNIQUE NOT NULL,
      muscle_group TEXT,
      equipment TEXT,
      difficulty_level TEXT,
      instructions TEXT,
      category TEXT
    );
    """)

    # 2. Gather existing exercise names for deduplication
    existing_names = set()
    
    # Query distinct exercise names from the exercises session logs table
    try:
        cursor.execute("SELECT DISTINCT exercise_name FROM exercises")
        for row in cursor.fetchall():
            if row["exercise_name"]:
                existing_names.add(row["exercise_name"].strip().lower())
    except sqlite3.OperationalError:
        print("Note: 'exercises' session logs table not found or empty.")

    # Query distinct exercise names from the exercise_library table itself
    try:
        cursor.execute("SELECT DISTINCT name FROM exercise_library")
        for row in cursor.fetchall():
            if row["name"]:
                existing_names.add(row["name"].strip().lower())
    except sqlite3.OperationalError:
        print("Note: 'exercise_library' table not initialized yet.")

    print(f"Collected {len(existing_names)} existing exercise names to deduplicate against.")

    # 3. Fetch exercise database JSON
    print("Fetching exercises from free-exercise-db on GitHub...")
    try:
        req = urllib.request.Request(
            JSON_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            exercises_data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching data: {e}")
        conn.close()
        return

    print(f"Retrieved {len(exercises_data)} exercises. Processing and filtering...")

    records_to_insert = []
    
    for exercise in exercises_data:
        name = exercise.get("name", "").strip()
        if not name:
            continue
            
        # Deduplicate
        name_lower = name.lower()
        if name_lower in existing_names:
            continue

        # Keep track of local duplicates to prevent double-inserting in the same run
        existing_names.add(name_lower)

        # Process columns
        primary_muscles = exercise.get("primaryMuscles", [])
        muscle_group = ", ".join(primary_muscles) if isinstance(primary_muscles, list) else ""
        
        equipment = exercise.get("equipment") or "body only"
        difficulty_level = exercise.get("level") or "beginner"
        
        instructions_list = exercise.get("instructions", [])
        if isinstance(instructions_list, list):
            instructions_str = " ".join(instructions_list)
        else:
            instructions_str = str(instructions_list)
            
        # Truncate instructions if they are too long to fit 'instructions (short)'
        if len(instructions_str) > 500:
            instructions_str = instructions_str[:497] + "..."
            
        category = exercise.get("category") or "strength"

        records_to_insert.append((
            name,
            muscle_group,
            equipment,
            difficulty_level,
            instructions_str,
            category
        ))

        # Stop when we reach 100-150 new exercises as per the requirement
        if len(records_to_insert) >= 150:
            break

    print(f"Inserting {len(records_to_insert)} new unique exercises into exercise_library...")
    
    if records_to_insert:
        cursor.executemany("""
            INSERT OR IGNORE INTO exercise_library (
                name, muscle_group, equipment, difficulty_level, instructions, category
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, records_to_insert)
        conn.commit()

    # 4. Verification
    cursor.execute("SELECT COUNT(*) as total_count FROM exercise_library")
    total_count = cursor.fetchone()["total_count"]
    print(f"\nVerification Results:")
    print(f"Total row count in exercise_library table: {total_count}")

    # Fetch and print a 5-row sample
    cursor.execute("""
        SELECT name, muscle_group, equipment, difficulty_level, instructions, category 
        FROM exercise_library 
        ORDER BY id ASC 
        LIMIT 5
    """)
    rows = cursor.fetchall()
    print("\n--- 5-Row Sample of Seeded Data ---")
    for idx, row in enumerate(rows, 1):
        print(f"\nExercise {idx}:")
        print(f"  Name: {row['name']}")
        print(f"  Muscle Group: {row['muscle_group']}")
        print(f"  Equipment: {row['equipment']}")
        print(f"  Difficulty: {row['difficulty_level']}")
        print(f"  Instructions (short): {row['instructions']}")
        print(f"  Category: {row['category']}")

    conn.close()

if __name__ == "__main__":
    seed_database()
