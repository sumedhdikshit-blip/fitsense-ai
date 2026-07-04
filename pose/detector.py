import cv2
import mediapipe as mp
import numpy as np

LANDMARK_MAP = {
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_elbow": 13,
    "right_elbow": 14,
    "left_wrist": 15,
    "right_wrist": 16,
    "left_hip": 23,
    "right_hip": 24,
    "left_knee": 25,
    "right_knee": 26,
    "left_ankle": 27,
    "right_ankle": 28,
}

def calculate_angle(a, b, c):
    """
    a, b, c are [x, y] coordinates. b is the vertex.
    Calculates angle at b using dot product (numerically stable).
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    ba = a - b
    bc = c - b
    
    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)
    
    if norm_ba == 0 or norm_bc == 0:
        return 0.0
        
    cosine_angle = np.dot(ba, bc) / (norm_ba * norm_bc)
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return float(np.degrees(angle))

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils

    def process_frame(self, frame_bgr):
        # Convert to RGB
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)
        return results

    def get_landmarks_dict(self, results):
        if not results or not results.pose_landmarks:
            return None
        
        landmarks = results.pose_landmarks.landmark
        coords = {}
        for name, idx in LANDMARK_MAP.items():
            if idx < len(landmarks):
                # We store x, y coordinates
                coords[name] = [landmarks[idx].x, landmarks[idx].y]
        return coords

    def draw_skeleton(self, frame_bgr, results):
        if results and results.pose_landmarks:
            self.mp_draw.draw_landmarks(
                frame_bgr,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_draw.DrawingSpec(color=(80, 110, 10), thickness=2, circle_radius=2), # circle spec
                self.mp_draw.DrawingSpec(color=(0, 200, 83), thickness=2, circle_radius=2)   # connection spec (accent green #00C853)
            )
        return frame_bgr
