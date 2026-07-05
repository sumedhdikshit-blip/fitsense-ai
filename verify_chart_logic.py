"""
Simulate the chart label logic to verify the fix produces correct, distinct dates.
"""

def simulate_chart_labels(data, MAX_LABELS=5):
    """Mirror the fixed JS logic from app.js drawWeightChart()"""
    num_points = len(data)
    if num_points == 0:
        return []
    
    label_indices = set()
    label_indices.add(0)
    label_indices.add(num_points - 1)
    
    if num_points <= MAX_LABELS:
        # Show every point when few entries
        for i in range(num_points):
            label_indices.add(i)
    else:
        # Evenly space (MAX_LABELS - 2) interior labels
        interior = MAX_LABELS - 2
        for k in range(1, interior + 1):
            label_indices.add(round(k * (num_points - 1) / (interior + 1)))
    
    labels = []
    for idx, point in enumerate(data):
        if idx in label_indices:
            date = point['date']
            parts = date.split('-')
            formatted = f"{parts[1]}/{parts[2]}" if len(parts) == 3 else date
            labels.append({'idx': idx, 'date': date, 'label': formatted, 'weight': point['weight_kg']})
    
    return labels

# Test data: 7 entries spanning June 10 - July 4 (matching what's in the DB)
all_data = [
    {'date': '2026-06-10', 'weight_kg': 83.5},
    {'date': '2026-06-18', 'weight_kg': 82.8},
    {'date': '2026-06-20', 'weight_kg': 82.0},
    {'date': '2026-06-25', 'weight_kg': 82.0},
    {'date': '2026-07-02', 'weight_kg': 81.5},
    {'date': '2026-07-03', 'weight_kg': 80.8},
    {'date': '2026-07-04', 'weight_kg': 80.0},
]

# Simulate different range filters
ranges = {
    '7D':  [d for d in all_data if d['date'] >= '2026-06-27'],
    '30D': [d for d in all_data if d['date'] >= '2026-06-04'],
    '90D': [d for d in all_data if d['date'] >= '2026-04-05'],
    'ALL': all_data,
}

print("=== Chart Label Simulation (Fixed Logic) ===\n")
for range_name, data in ranges.items():
    labels = simulate_chart_labels(data)
    print(f"Range: {range_name} ({len(data)} points)")
    for lbl in labels:
        print(f"  idx={lbl['idx']:2d}  date={lbl['date']}  label={lbl['label']}  weight={lbl['weight']} kg")
    
    # Check for duplicate labels
    label_strs = [lbl['label'] for lbl in labels]
    dupes = [l for l in label_strs if label_strs.count(l) > 1]
    if dupes:
        print(f"  *** DUPLICATE LABELS FOUND: {set(dupes)} ***")
    else:
        print(f"  OK: All {len(labels)} labels are distinct")
    print()

print("=== OLD buggy logic simulation ===\n")
def simulate_old_logic(data):
    """Mirror the OLD buggy JS logic"""
    num_points = len(data)
    labels = []
    for idx, point in enumerate(data):
        if num_points <= 7 or idx == 0 or idx == num_points - 1 or idx == num_points // 2:
            date = point['date']
            parts = date.split('-')
            formatted = f"{parts[1]}/{parts[2]}" if len(parts) == 3 else date
            labels.append({'idx': idx, 'label': formatted})
    return labels

for range_name, data in ranges.items():
    labels = simulate_old_logic(data)
    label_strs = [lbl['label'] for lbl in labels]
    dupes = [l for l in label_strs if label_strs.count(l) > 1]
    print(f"Range: {range_name} ({len(data)} points) -> labels: {[l['label'] for l in labels]}")
    if dupes:
        print(f"  *** DUPLICATE LABELS: {set(dupes)} ***")
