EXERCISE_LIBRARY = {
    "squat": {
        "display_name": "Squat",
        "category": "lower_body",
        "met_value": 5.0,
        "angles": {
            "left_knee": ["left_hip", "left_knee", "left_ankle"],
            "right_knee": ["right_hip", "right_knee", "right_ankle"],
            "hip": ["left_shoulder", "left_hip", "left_knee"],
            "back": ["left_shoulder", "left_hip", "left_ankle"]
        },
        "primary_angle": "left_knee",
        "down_threshold": 90,
        "up_threshold": 160,
        "form_rules": [
            {"name": "Knees caving in", "check": "knee_alignment_x", "severity": "RED"},
            {"name": "Not deep enough", "check": "primary_angle_gt_at_bottom:110", "severity": "YELLOW"},
            {"name": "Forward lean", "check": "back_angle_lt:45", "severity": "YELLOW"}
        ]
    },
    "pushup": {
        "display_name": "Pushup",
        "category": "upper_body",
        "met_value": 8.0,
        "angles": {
            "left_elbow": ["left_shoulder", "left_elbow", "left_wrist"],
            "right_elbow": ["right_shoulder", "right_elbow", "right_wrist"],
            "back": ["left_shoulder", "left_hip", "left_ankle"]
        },
        "primary_angle": "left_elbow",
        "down_threshold": 90,
        "up_threshold": 160,
        "form_rules": [
            {"name": "Not deep enough", "check": "primary_angle_gt_at_bottom:110", "severity": "YELLOW"},
            {"name": "Sagging hips", "check": "back_angle_lt:140", "severity": "RED"},
            {"name": "High hips", "check": "back_angle_gt:190", "severity": "YELLOW"}
        ]
    },
    "bicep_curl": {
        "display_name": "Bicep Curl",
        "category": "upper_body",
        "met_value": 3.0,
        "angles": {
            "left_elbow": ["left_shoulder", "left_elbow", "left_wrist"],
            "right_elbow": ["right_shoulder", "right_elbow", "right_wrist"],
            "back": ["left_shoulder", "left_hip", "left_ankle"]
        },
        "primary_angle": "left_elbow",
        "down_threshold": 150,
        "up_threshold": 40,
        "form_rules": [
            {"name": "Incomplete curl", "check": "primary_angle_gt_at_top:60", "severity": "YELLOW"},
            {"name": "Incomplete extension", "check": "primary_angle_lt_at_bottom:130", "severity": "YELLOW"},
            {"name": "Swinging back", "check": "back_angle_lt:160", "severity": "RED"}
        ]
    }
}
