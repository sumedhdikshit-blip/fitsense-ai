import sqlite3, json

conn = sqlite3.connect('fitsense.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Check all weight history
c.execute('SELECT entry_id, user_id, date, weight_kg, created_at FROM weight_history ORDER BY date ASC')
rows = c.fetchall()
print('=== weight_history table ===')
for r in rows:
    print(dict(r))

# Simulate the API query for different day ranges
print()
print('=== days=7 ===')
c.execute("SELECT date, weight_kg FROM weight_history WHERE user_id = 1 AND date >= date('now', '-7 days') ORDER BY date ASC")
for r in c.fetchall():
    print(dict(r))

print()
print('=== days=30 ===')
c.execute("SELECT date, weight_kg FROM weight_history WHERE user_id = 1 AND date >= date('now', '-30 days') ORDER BY date ASC")
for r in c.fetchall():
    print(dict(r))

print()
print('=== days=all ===')
c.execute('SELECT date, weight_kg FROM weight_history WHERE user_id = 1 ORDER BY date ASC')
for r in c.fetchall():
    print(dict(r))

conn.close()
