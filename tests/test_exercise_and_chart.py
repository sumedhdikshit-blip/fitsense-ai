import os
import ast
import pytest
from datetime import datetime, timedelta

# Add fitsense-ai workspace to path to import config
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.exercise_library import EXERCISE_LIBRARY

# ==================== EXERCISE LIBRARY TESTS ====================

def test_no_duplicate_keys_in_exercise_library_file():
    """Ensure there are no duplicate dictionary keys defined in config/exercise_library.py"""
    filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "exercise_library.py")
    
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
        
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == "EXERCISE_LIBRARY":
            keys = []
            for k in node.value.keys:
                if isinstance(k, ast.Constant):
                    keys.append(k.value)
                elif isinstance(k, ast.Str): # Python < 3.8 compatibility
                    keys.append(k.s)
            
            seen = set()
            duplicates = []
            for key in keys:
                if key in seen:
                    duplicates.append(key)
                seen.add(key)
                
            assert not duplicates, f"Duplicate keys found in EXERCISE_LIBRARY source: {duplicates}"

def test_exercise_library_schema_and_required_fields():
    """Verify that every exercise has a display name, valid category, and all required keys."""
    required_keys = [
        "display_name", "category", "met_value", "mode", "angles",
        "primary_angle", "down_threshold", "up_threshold", "form_rules", "description"
    ]
    
    valid_categories = {
        "upper_body", "lower_body", "core", "cardio", "flexibility", "triceps", "biceps", "shoulders"
    }
    
    for key, val in EXERCISE_LIBRARY.items():
        # Check required fields
        for req in required_keys:
            assert req in val, f"Exercise '{key}' is missing required field '{req}'"
            
        # Check display name is valid
        assert val["display_name"] and isinstance(val["display_name"], str), f"Exercise '{key}' has invalid display_name"
        
        # Check category is valid
        assert val["category"] in valid_categories, f"Exercise '{key}' has invalid category tag '{val['category']}'"
        
        # Check types
        assert isinstance(val["met_value"], (int, float)), f"Exercise '{key}' met_value must be numeric"
        assert val["mode"] in ("rep", "hold"), f"Exercise '{key}' mode must be 'rep' or 'hold'"
        assert isinstance(val["angles"], dict), f"Exercise '{key}' angles must be a dict"
        assert isinstance(val["form_rules"], list), f"Exercise '{key}' form_rules must be a list"


# ==================== WEIGHT CHART LABEL TESTS ====================

def simulate_js_chart_labeling(data, MAX_LABELS=5):
    """Python translation of the fixed Javascript labeling logic from app.js"""
    num_points = len(data)
    if num_points == 0:
        return []
        
    label_indices = set()
    label_indices.add(0)
    label_indices.add(num_points - 1)
    
    if num_points <= MAX_LABELS:
        for i in range(num_points):
            label_indices.add(i)
    else:
        interior = MAX_LABELS - 2
        for k in range(1, interior + 1):
            label_indices.add(round(k * (num_points - 1) / (interior + 1)))
            
    labels = []
    for idx, point in enumerate(data):
        if idx in label_indices:
            date_str = point["date"]
            parts = date_str.split("-")
            formatted = f"{parts[1]}/{parts[2]}" if len(parts) == 3 else date_str
            labels.append(formatted)
    return labels

def test_chart_logic_no_duplicates_small_datasets():
    """Verify that small datasets never produce duplicate date labels or overlap issues."""
    for n in range(1, 6):
        test_data = [{"date": f"2026-07-{i:02d}", "weight_kg": 80.0 + i} for i in range(1, n + 1)]
        labels = simulate_js_chart_labeling(test_data)
        
        # The number of labels should equal the number of points
        assert len(labels) == n
        # Every label must be unique
        assert len(labels) == len(set(labels)), f"Duplicate labels in small dataset size {n}: {labels}"

def test_chart_logic_no_duplicates_large_datasets():
    """Verify that large datasets select at most MAX_LABELS (5) distinct labels."""
    test_data = [{"date": f"2026-07-{i:02d}", "weight_kg": 75.0} for i in range(1, 31)]
    labels = simulate_js_chart_labeling(test_data)
    
    assert len(labels) <= 5
    assert len(labels) == len(set(labels)), f"Duplicate labels in large dataset: {labels}"

def test_chart_logic_calendar_edge_cases():
    """Verify distinct and correct labeling across month boundaries, leap years, and DST switches."""
    
    # 1. Month boundaries (October 28 to November 3)
    month_boundary_data = [
        {"date": "2026-10-28", "weight_kg": 70.0},
        {"date": "2026-10-29", "weight_kg": 70.2},
        {"date": "2026-10-30", "weight_kg": 70.4},
        {"date": "2026-10-31", "weight_kg": 70.6},
        {"date": "2026-11-01", "weight_kg": 70.8},
        {"date": "2026-11-02", "weight_kg": 71.0},
        {"date": "2026-11-03", "weight_kg": 71.2},
    ]
    labels_mb = simulate_js_chart_labeling(month_boundary_data)
    assert len(labels_mb) == len(set(labels_mb)), f"Duplicates in month boundary: {labels_mb}"
    assert "10/31" in labels_mb
    assert "11/01" in labels_mb or "11/02" in labels_mb
    
    # 2. Leap year boundary (Feb 27 to Mar 2, 2024 - Leap Year)
    leap_year_data = [
        {"date": "2024-02-27", "weight_kg": 75.0},
        {"date": "2024-02-28", "weight_kg": 75.1},
        {"date": "2024-02-29", "weight_kg": 75.2}, # Leap day
        {"date": "2024-03-01", "weight_kg": 75.3},
        {"date": "2024-03-02", "weight_kg": 75.4},
    ]
    labels_ly = simulate_js_chart_labeling(leap_year_data)
    assert len(labels_ly) == len(set(labels_ly)), f"Duplicates in leap year data: {labels_ly}"
    assert "02/29" in labels_ly
    assert "03/01" in labels_ly

    # 3. Daylight Savings Time transition dates (March 8, 2026 - DST Start)
    dst_data = [
        {"date": "2026-03-06", "weight_kg": 81.0},
        {"date": "2026-03-07", "weight_kg": 81.2},
        {"date": "2026-03-08", "weight_kg": 81.4}, # DST transition
        {"date": "2026-03-09", "weight_kg": 81.6},
        {"date": "2026-03-10", "weight_kg": 81.8},
    ]
    labels_dst = simulate_js_chart_labeling(dst_data)
    assert len(labels_dst) == len(set(labels_dst)), f"Duplicates in DST data: {labels_dst}"
    assert "03/08" in labels_dst
