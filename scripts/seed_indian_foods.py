import sqlite3
import os

DB_PATH = "fitsense.db"

indian_foods = [
    {
        "name": "Low-fat paneer",
        "serving_description": "100g",
        "calories": 160.0,
        "protein_g": 20.0,
        "carbs_g": 4.5,
        "fat_g": 7.0,
        "saturated_fat_g": 4.2,
        "fiber_g": 0.0,
        "sodium_mg": 20.0,
        "sugar_g": 3.5,
        "calcium_mg": 350.0,
        "iron_mg": 0.1,
        "vitamin_c_mg": 0.0,
        "meal_category": None
    },
    {
        "name": "Regular paneer",
        "serving_description": "100g",
        "calories": 265.0,
        "protein_g": 18.0,
        "carbs_g": 3.5,
        "fat_g": 20.0,
        "saturated_fat_g": 12.0,
        "fiber_g": 0.0,
        "sodium_mg": 20.0,
        "sugar_g": 3.0,
        "calcium_mg": 480.0,
        "iron_mg": 0.2,
        "vitamin_c_mg": 0.0,
        "meal_category": None
    },
    {
        "name": "Soya chunks",
        "serving_description": "100g prepared",
        "calories": 140.0,
        "protein_g": 18.0,
        "carbs_g": 10.0,
        "fat_g": 0.5,
        "saturated_fat_g": 0.1,
        "fiber_g": 4.0,
        "sodium_mg": 10.0,
        "sugar_g": 2.0,
        "calcium_mg": 120.0,
        "iron_mg": 6.0,
        "vitamin_c_mg": 0.0,
        "meal_category": None
    },
    {
        "name": "Tempeh",
        "serving_description": "100g",
        "calories": 193.0,
        "protein_g": 19.0,
        "carbs_g": 9.0,
        "fat_g": 11.0,
        "saturated_fat_g": 3.0,
        "fiber_g": 3.8,
        "sodium_mg": 9.0,
        "sugar_g": 0.5,
        "calcium_mg": 111.0,
        "iron_mg": 2.7,
        "vitamin_c_mg": 0.0,
        "meal_category": "snacks"
    },
    {
        "name": "Tofu",
        "serving_description": "100g",
        "calories": 76.0,
        "protein_g": 8.0,
        "carbs_g": 1.9,
        "fat_g": 4.8,
        "saturated_fat_g": 0.7,
        "fiber_g": 0.3,
        "sodium_mg": 7.0,
        "sugar_g": 0.5,
        "calcium_mg": 350.0,
        "iron_mg": 5.4,
        "vitamin_c_mg": 0.1,
        "meal_category": "snacks"
    },
    {
        "name": "Dal fry",
        "serving_description": "100g",
        "calories": 115.0,
        "protein_g": 5.0,
        "carbs_g": 16.0,
        "fat_g": 3.5,
        "saturated_fat_g": 1.5,
        "fiber_g": 4.5,
        "sodium_mg": 350.0,
        "sugar_g": 1.0,
        "calcium_mg": 40.0,
        "iron_mg": 1.2,
        "vitamin_c_mg": 1.0,
        "meal_category": "lunch"
    },
    {
        "name": "Chole (chickpea curry)",
        "serving_description": "100g",
        "calories": 130.0,
        "protein_g": 4.5,
        "carbs_g": 18.0,
        "fat_g": 4.5,
        "saturated_fat_g": 1.0,
        "fiber_g": 5.0,
        "sodium_mg": 400.0,
        "sugar_g": 2.0,
        "calcium_mg": 50.0,
        "iron_mg": 1.8,
        "vitamin_c_mg": 2.0,
        "meal_category": "lunch"
    },
    {
        "name": "Rajma (kidney bean curry)",
        "serving_description": "100g",
        "calories": 120.0,
        "protein_g": 4.8,
        "carbs_g": 16.0,
        "fat_g": 4.0,
        "saturated_fat_g": 1.2,
        "fiber_g": 5.5,
        "sodium_mg": 380.0,
        "sugar_g": 1.5,
        "calcium_mg": 45.0,
        "iron_mg": 1.5,
        "vitamin_c_mg": 1.5,
        "meal_category": "lunch"
    },
    {
        "name": "Roti / chapati",
        "serving_description": "100g (approx. 3 rotis)",
        "calories": 260.0,
        "protein_g": 8.5,
        "carbs_g": 52.0,
        "fat_g": 3.0,
        "saturated_fat_g": 0.5,
        "fiber_g": 6.5,
        "sodium_mg": 150.0,
        "sugar_g": 0.5,
        "calcium_mg": 40.0,
        "iron_mg": 2.5,
        "vitamin_c_mg": 0.0,
        "meal_category": None
    },
    {
        "name": "Brown rice",
        "serving_description": "100g cooked",
        "calories": 111.0,
        "protein_g": 2.6,
        "carbs_g": 23.0,
        "fat_g": 0.9,
        "saturated_fat_g": 0.2,
        "fiber_g": 1.8,
        "sodium_mg": 5.0,
        "sugar_g": 0.1,
        "calcium_mg": 10.0,
        "iron_mg": 0.4,
        "vitamin_c_mg": 0.0,
        "meal_category": None
    },
    {
        "name": "Idli",
        "serving_description": "100g (approx. 2.5 idlis)",
        "calories": 120.0,
        "protein_g": 3.5,
        "carbs_g": 25.0,
        "fat_g": 0.5,
        "saturated_fat_g": 0.1,
        "fiber_g": 1.5,
        "sodium_mg": 200.0,
        "sugar_g": 0.2,
        "calcium_mg": 15.0,
        "iron_mg": 0.5,
        "vitamin_c_mg": 0.0,
        "meal_category": "breakfast"
    },
    {
        "name": "Dosa (plain)",
        "serving_description": "100g",
        "calories": 168.0,
        "protein_g": 3.8,
        "carbs_g": 29.0,
        "fat_g": 3.5,
        "saturated_fat_g": 0.8,
        "fiber_g": 1.8,
        "sodium_mg": 220.0,
        "sugar_g": 0.3,
        "calcium_mg": 18.0,
        "iron_mg": 0.6,
        "vitamin_c_mg": 0.0,
        "meal_category": "breakfast"
    },
    {
        "name": "Poha",
        "serving_description": "100g cooked",
        "calories": 180.0,
        "protein_g": 3.0,
        "carbs_g": 32.0,
        "fat_g": 4.5,
        "saturated_fat_g": 1.0,
        "fiber_g": 2.5,
        "sodium_mg": 280.0,
        "sugar_g": 1.2,
        "calcium_mg": 30.0,
        "iron_mg": 3.5,
        "vitamin_c_mg": 5.0,
        "meal_category": "breakfast"
    },
    {
        "name": "Upma",
        "serving_description": "100g cooked",
        "calories": 172.0,
        "protein_g": 3.5,
        "carbs_g": 28.0,
        "fat_g": 5.0,
        "saturated_fat_g": 1.5,
        "fiber_g": 2.0,
        "sodium_mg": 320.0,
        "sugar_g": 1.0,
        "calcium_mg": 25.0,
        "iron_mg": 1.2,
        "vitamin_c_mg": 2.0,
        "meal_category": "breakfast"
    },
    {
        "name": "Sprouts salad",
        "serving_description": "100g",
        "calories": 95.0,
        "protein_g": 6.0,
        "carbs_g": 14.0,
        "fat_g": 1.0,
        "saturated_fat_g": 0.2,
        "fiber_g": 4.0,
        "sodium_mg": 120.0,
        "sugar_g": 2.5,
        "calcium_mg": 40.0,
        "iron_mg": 1.5,
        "vitamin_c_mg": 12.0,
        "meal_category": "snacks"
    },
    {
        "name": "Curd/dahi (plain)",
        "serving_description": "100g",
        "calories": 60.0,
        "protein_g": 3.2,
        "carbs_g": 4.3,
        "fat_g": 3.3,
        "saturated_fat_g": 2.1,
        "fiber_g": 0.0,
        "sodium_mg": 45.0,
        "sugar_g": 4.0,
        "calcium_mg": 120.0,
        "iron_mg": 0.1,
        "vitamin_c_mg": 0.5,
        "meal_category": None
    },
    {
        "name": "Sambar",
        "serving_description": "100g",
        "calories": 65.0,
        "protein_g": 2.2,
        "carbs_g": 10.0,
        "fat_g": 1.8,
        "saturated_fat_g": 0.5,
        "fiber_g": 2.2,
        "sodium_mg": 300.0,
        "sugar_g": 2.0,
        "calcium_mg": 35.0,
        "iron_mg": 0.8,
        "vitamin_c_mg": 4.0,
        "meal_category": "lunch"
    },
    {
        "name": "Palak paneer",
        "serving_description": "100g",
        "calories": 125.0,
        "protein_g": 6.5,
        "carbs_g": 4.0,
        "fat_g": 9.5,
        "saturated_fat_g": 5.5,
        "fiber_g": 2.0,
        "sodium_mg": 350.0,
        "sugar_g": 1.2,
        "calcium_mg": 220.0,
        "iron_mg": 2.0,
        "vitamin_c_mg": 8.0,
        "meal_category": "lunch"
    },
    {
        "name": "Rice + dal khichdi",
        "serving_description": "100g",
        "calories": 140.0,
        "protein_g": 4.2,
        "carbs_g": 24.0,
        "fat_g": 3.0,
        "saturated_fat_g": 1.2,
        "fiber_g": 2.8,
        "sodium_mg": 280.0,
        "sugar_g": 0.5,
        "calcium_mg": 22.0,
        "iron_mg": 1.0,
        "vitamin_c_mg": 0.5,
        "meal_category": "lunch"
    },
    {
        "name": "Besan chilla",
        "serving_description": "100g",
        "calories": 198.0,
        "protein_g": 9.0,
        "carbs_g": 24.0,
        "fat_g": 7.0,
        "saturated_fat_g": 1.0,
        "fiber_g": 4.5,
        "sodium_mg": 340.0,
        "sugar_g": 1.8,
        "calcium_mg": 60.0,
        "iron_mg": 2.8,
        "vitamin_c_mg": 3.0,
        "meal_category": "breakfast"
    },
    {
        "name": "Mustard oil",
        "serving_description": "100g (100ml)",
        "calories": 884.0,
        "protein_g": 0.0,
        "carbs_g": 0.0,
        "fat_g": 100.0,
        "saturated_fat_g": 11.6,
        "fiber_g": 0.0,
        "sodium_mg": 0.0,
        "sugar_g": 0.0,
        "calcium_mg": 0.0,
        "iron_mg": 0.0,
        "vitamin_c_mg": 0.0,
        "meal_category": None
    },
    {
        "name": "Coconut oil",
        "serving_description": "100g (100ml)",
        "calories": 884.0,
        "protein_g": 0.0,
        "carbs_g": 0.0,
        "fat_g": 100.0,
        "saturated_fat_g": 82.5,
        "fiber_g": 0.0,
        "sodium_mg": 0.0,
        "sugar_g": 0.0,
        "calcium_mg": 0.0,
        "iron_mg": 0.0,
        "vitamin_c_mg": 0.0,
        "meal_category": None
    },
    {
        "name": "Sunflower oil",
        "serving_description": "100g (100ml)",
        "calories": 884.0,
        "protein_g": 0.0,
        "carbs_g": 0.0,
        "fat_g": 100.0,
        "saturated_fat_g": 13.0,
        "fiber_g": 0.0,
        "sodium_mg": 0.0,
        "sugar_g": 0.0,
        "calcium_mg": 0.0,
        "iron_mg": 0.0,
        "vitamin_c_mg": 0.0,
        "meal_category": None
    },
    {
        "name": "Ghee",
        "serving_description": "100g",
        "calories": 884.0,
        "protein_g": 0.0,
        "carbs_g": 0.0,
        "fat_g": 99.8,
        "saturated_fat_g": 62.0,
        "fiber_g": 0.0,
        "sodium_mg": 2.0,
        "sugar_g": 0.0,
        "calcium_mg": 4.0,
        "iron_mg": 0.0,
        "vitamin_c_mg": 0.0,
        "meal_category": None
    },
    {
        "name": "Butter",
        "serving_description": "100g",
        "calories": 717.0,
        "protein_g": 0.9,
        "carbs_g": 0.1,
        "fat_g": 81.0,
        "saturated_fat_g": 51.0,
        "fiber_g": 0.0,
        "sodium_mg": 643.0,
        "sugar_g": 0.1,
        "calcium_mg": 24.0,
        "iron_mg": 0.02,
        "vitamin_c_mg": 0.0,
        "meal_category": None
    },
    {
        "name": "White butter (makhkhan)",
        "serving_description": "100g",
        "calories": 740.0,
        "protein_g": 0.8,
        "carbs_g": 0.5,
        "fat_g": 82.0,
        "saturated_fat_g": 52.0,
        "fiber_g": 0.0,
        "sodium_mg": 10.0,
        "sugar_g": 0.5,
        "calcium_mg": 20.0,
        "iron_mg": 0.02,
        "vitamin_c_mg": 0.0,
        "meal_category": None
    },
    {
        "name": "Buttermilk (chaas)",
        "serving_description": "100g",
        "calories": 25.0,
        "protein_g": 1.2,
        "carbs_g": 2.0,
        "fat_g": 1.0,
        "saturated_fat_g": 0.6,
        "fiber_g": 0.0,
        "sodium_mg": 150.0,
        "sugar_g": 1.8,
        "calcium_mg": 45.0,
        "iron_mg": 0.05,
        "vitamin_c_mg": 0.2,
        "meal_category": None
    }
]

def seed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    added_count = 0
    skipped_count = 0
    
    for food in indian_foods:
        # Check if duplicate exists
        cursor.execute("SELECT COUNT(*) FROM food_database WHERE name = ?", (food["name"],))
        if cursor.fetchone()[0] > 0:
            skipped_count += 1
            print(f"Skipping duplicate: {food['name']}")
            continue
            
        cursor.execute("""
            INSERT INTO food_database (
                name, serving_description, calories, protein_g, carbs_g, fat_g,
                saturated_fat_g, fiber_g, sodium_mg, sugar_g, calcium_mg, iron_mg,
                vitamin_c_mg, meal_category
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            food["name"], food["serving_description"], food["calories"], food["protein_g"],
            food["carbs_g"], food["fat_g"], food["saturated_fat_g"], food["fiber_g"],
            food["sodium_mg"], food["sugar_g"], food["calcium_mg"], food["iron_mg"],
            food["vitamin_c_mg"], food["meal_category"]
        ))
        added_count += 1
        
    conn.commit()
    
    # Verify row counts and print sample
    cursor.execute("SELECT COUNT(*) FROM food_database")
    total_count = cursor.fetchone()[0]
    
    print(f"\nSeed Complete. Added {added_count} items. Skipped {skipped_count} items. Total items in food_database: {total_count}")
    
    print("\nSample of 5 newly added items:")
    cursor.execute("""
        SELECT name, calories, protein_g, carbs_g, fat_g, meal_category 
        FROM food_database 
        ORDER BY food_id DESC 
        LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"- Name: {row[0]}, Calories: {row[1]}, P: {row[2]}g, C: {row[3]}g, F: {row[4]}g, Category: {row[5]}")
        
    conn.close()

if __name__ == "__main__":
    seed()
