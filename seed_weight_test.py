"""
Seed 4 distinct weight log dates spanning 3+ weeks for testing the chart bug fix.
Run this BEFORE starting the server, then check the chart.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fitsense.db")

test_entries = [
    ("2026-06-10", 83.5),   # ~3.5 weeks ago
    ("2026-06-18", 82.8),   # ~2.5 weeks ago
    ("2026-06-25", 82.0),   # ~1.5 weeks ago
    ("2026-07-02", 81.5),   # ~2 days ago
    ("2026-07-03", 80.8),   # yesterday
    ("2026-07-04", 80.0),   # today
]

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

for date, weight in test_entries:
    c.execute("""
        INSERT INTO weight_history (user_id, date, weight_kg)
        VALUES (1, ?, ?)
        ON CONFLICT(user_id, date) DO UPDATE SET weight_kg = excluded.weight_kg
    """, (date, weight))
    print(f"  Upserted: {date} -> {weight} kg")

conn.commit()

# Verify
print("\n=== Final weight_history ===")
c.execute("SELECT date, weight_kg FROM weight_history WHERE user_id = 1 ORDER BY date ASC")
for r in c.fetchall():
    print(f"  {r['date']}  {r['weight_kg']} kg")

conn.close()
print("\nDone.")
