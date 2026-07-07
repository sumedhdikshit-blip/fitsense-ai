# FitSense AI — Food Database Seeding Script

import os
import sqlite3
import csv
import urllib.request
import io

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fitsense.db")
CSV_URL = "https://corgis-edu.github.io/corgis/datasets/csv/food/food.csv"

def seed_database():
    print("Connecting to database...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create table if not exists (in case it wasn't run via init_db)
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
      vitamin_c_mg REAL
    );
    """)

    # 2. Check if already seeded to ensure idempotency
    cursor.execute("SELECT COUNT(*) as cnt FROM food_database")
    count = cursor.fetchone()[0]
    if count >= 1000:
        print(f"Database already contains {count} food items. Skipping seeding.")
        conn.close()
        return

    print("Fetching nutrition data from CORGIS Food Dataset...")
    try:
        req = urllib.request.Request(
            CSV_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            csv_data = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching data: {e}")
        conn.close()
        return

    print("Parsing CSV and seeding food items...")
    reader = csv.DictReader(io.StringIO(csv_data))
    
    # We will clear table first if there's any partial data
    cursor.execute("DELETE FROM food_database")
    
    records_to_insert = []
    
    for row in reader:
        name = row.get("Description", "").strip()
        if not name:
            continue
            
        try:
            protein = float(row.get("Data.Protein", 0.0))
            carbs = float(row.get("Data.Carbohydrate", 0.0))
            fat = float(row.get("Data.Fat.Total Lipid", 0.0))
            
            # Calorie calculation via standard Atwater factors (4-4-9 method)
            calories = round(4.0 * protein + 4.0 * carbs + 9.0 * fat, 1)
            
            saturated_fat = float(row.get("Data.Fat.Saturated Fat", 0.0))
            fiber = float(row.get("Data.Fiber", 0.0))
            sodium = float(row.get("Data.Major Minerals.Sodium", 0.0))
            sugar = float(row.get("Data.Sugar Total", 0.0))
            calcium = float(row.get("Data.Major Minerals.Calcium", 0.0))
            iron = float(row.get("Data.Major Minerals.Iron", 0.0))
            vitamin_c = float(row.get("Data.Vitamins.Vitamin C", 0.0))
            
            records_to_insert.append((
                name,
                "100g",
                calories,
                protein,
                carbs,
                fat,
                saturated_fat,
                fiber,
                sodium,
                sugar,
                calcium,
                iron,
                vitamin_c
            ))
        except (ValueError, TypeError) as parse_err:
            # Skip invalid/malformed rows
            continue

    print(f"Found {len(records_to_insert)} valid rows. Inserting into food_database...")
    
    # Insert in batches
    cursor.executemany("""
        INSERT INTO food_database (
            name, serving_description, calories, protein_g, carbs_g, fat_g, 
            saturated_fat_g, fiber_g, sodium_mg, sugar_g, calcium_mg, iron_mg, vitamin_c_mg
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records_to_insert)
    
    conn.commit()
    
    # Verify final count
    cursor.execute("SELECT COUNT(*) FROM food_database")
    final_count = cursor.fetchone()[0]
    print(f"Successfully seeded {final_count} food items into the database!")
    
    conn.close()

if __name__ == "__main__":
    seed_database()
