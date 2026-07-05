"""
Quick script to verify /weight/history API returns correct, distinct dates
for each range toggle.
"""
import urllib.request
import json

for days in ['7', '30', '90', 'all']:
    url = "http://127.0.0.1:8000/weight/history?days=" + days
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            data = json.loads(r.read())
        print("=== GET /weight/history?days=" + days + " === (" + str(len(data)) + " points)")
        for d in data:
            print("  date=" + str(d['date']) + "  weight=" + str(d['weight_kg']) + " kg")
        
        # Check for duplicates
        dates = [d['date'] for d in data]
        dupes = [dt for dt in dates if dates.count(dt) > 1]
        if dupes:
            print("  *** DUPLICATE DATES: " + str(set(dupes)) + " ***")
        else:
            print("  OK: All dates are distinct and unique")
        print()
    except Exception as e:
        print("Error for days=" + days + ": " + str(e))
        print()
