class RepCounter:
    def __init__(self, exercise_key, exercise_config):
        self.exercise_key = exercise_key
        self.config = exercise_config
        
        self.primary_angle = self.config["primary_angle"]
        self.down_threshold = self.config["down_threshold"]
        self.up_threshold = self.config["up_threshold"]
        
        self.reps_counted = 0
        self.stage = None  # Will be initialized on first update
        
        self.all_rep_scores = []
        self.avg_form_score = 100.0
        self.latest_feedback = [{"message": "Get ready!", "severity": "GREEN"}]
        
        # Rep-specific tracking
        self.rep_min_angles = {}
        self.rep_max_angles = {}
        self.rep_landmarks = []

    def reset_rep_tracking(self, current_angles=None):
        self.rep_min_angles = {}
        self.rep_max_angles = {}
        self.rep_landmarks = []
        if current_angles:
            for joint, val in current_angles.items():
                self.rep_min_angles[joint] = val
                self.rep_max_angles[joint] = val

    def update(self, current_angles, landmarks):
        """
        Processes new frame joint angles and coordinates.
        Returns True if a new rep was completed.
        """
        if not current_angles or self.primary_angle not in current_angles:
            return False
        
        angle = current_angles[self.primary_angle]
        
        # Initialize stage on first frame
        if self.stage is None:
            if self.down_threshold < self.up_threshold:
                self.stage = "up"
            else:
                self.stage = "down"
            self.reset_rep_tracking(current_angles)
            
        # Update min/max angles for the current rep
        for joint, val in current_angles.items():
            if joint not in self.rep_min_angles:
                self.rep_min_angles[joint] = val
                self.rep_max_angles[joint] = val
            else:
                self.rep_min_angles[joint] = min(self.rep_min_angles[joint], val)
                self.rep_max_angles[joint] = max(self.rep_max_angles[joint], val)
                
        # Store landmarks
        if landmarks:
            self.rep_landmarks.append(landmarks)
            
        rep_completed = False
        
        if self.down_threshold < self.up_threshold:
            # Case A: Squat / Pushup (down is smaller angle, up is larger angle)
            if self.stage == "up" and angle <= self.down_threshold:
                self.stage = "down"
            elif self.stage == "down" and angle >= self.up_threshold:
                self.stage = "up"
                rep_completed = True
        else:
            # Case B: Bicep Curl (down is larger angle, up is smaller angle)
            if self.stage == "down" and angle <= self.up_threshold:
                self.stage = "up"
                rep_completed = True
            elif self.stage == "up" and angle >= self.down_threshold:
                self.stage = "down"
                self.reset_rep_tracking(current_angles)
                
        if rep_completed:
            self.reps_counted += 1
            # Evaluate form rules for the completed rep
            rep_score, feedback = self.evaluate_form_rules()
            self.all_rep_scores.append(rep_score)
            self.avg_form_score = sum(self.all_rep_scores) / len(self.all_rep_scores)
            self.latest_feedback = feedback
            
            # Reset tracking for Squat/Pushup right after completion
            if self.down_threshold < self.up_threshold:
                self.reset_rep_tracking(current_angles)
                
        return rep_completed

    def evaluate_form_rules(self):
        feedback = []
        score = 100
        
        form_rules = self.config.get("form_rules", [])
        for rule in form_rules:
            check_str = rule["check"]
            severity = rule["severity"]
            rule_name = rule["name"]
            
            triggered = False
            
            if check_str == "knee_alignment_x":
                triggered = self._check_knee_alignment()
                
            elif ":" in check_str:
                cond, thresh_val = check_str.split(":")
                val = float(thresh_val)
                
                if cond.startswith("primary_angle"):
                    primary_key = self.primary_angle
                    min_val = self.rep_min_angles.get(primary_key, 180.0)
                    max_val = self.rep_max_angles.get(primary_key, 0.0)
                    
                    if cond == "primary_angle_gt_at_bottom":
                        # Failed to go low/deep enough (e.g. minimum angle is too high)
                        if min_val > val:
                            triggered = True
                    elif cond == "primary_angle_gt_at_top":
                        # Failed to curl high enough (e.g. minimum angle is too high)
                        if min_val > val:
                            triggered = True
                    elif cond == "primary_angle_lt_at_bottom":
                        # Failed to extend fully (e.g. maximum angle is too small)
                        if max_val < val:
                            triggered = True
                            
                elif "_angle_" in cond:
                    angle_name = cond.split("_angle_")[0]
                    min_val = self.rep_min_angles.get(angle_name, 180.0)
                    max_val = self.rep_max_angles.get(angle_name, 0.0)
                    op = cond.split("_angle_")[1]
                    
                    if op == "lt":
                        if min_val < val:
                            triggered = True
                    elif op == "gt":
                        if max_val > val:
                            triggered = True
            
            if triggered:
                deduction = 20 if severity == "RED" else 10
                score -= deduction
                feedback.append({"message": rule_name, "severity": severity})
                
        if score == 100:
            feedback.append({"message": "Good form!", "severity": "GREEN"})
            
        score = max(0, score)
        return score, feedback

    def _check_knee_alignment(self):
        """
        Check if knees cave in (knee_alignment_x) relative to hip width.
        Calculates distance from center line (mid-hip) to knee vs. mid-hip to hip.
        """
        caved_frames = 0
        total_frames = 0
        
        for lm in self.rep_landmarks:
            if not lm:
                continue
            left_hip = lm.get("left_hip")
            right_hip = lm.get("right_hip")
            left_knee = lm.get("left_knee")
            right_knee = lm.get("right_knee")
            
            if left_hip and right_hip and left_knee and right_knee:
                total_frames += 1
                center_x = (left_hip[0] + right_hip[0]) / 2.0
                
                # Check distances from mid-hip centerline
                left_hip_dist = abs(left_hip[0] - center_x)
                left_knee_dist = abs(left_knee[0] - center_x)
                
                right_hip_dist = abs(right_hip[0] - center_x)
                right_knee_dist = abs(right_knee[0] - center_x)
                
                # If knee is significantly closer to centerline than hip, they are caving in
                if left_knee_dist < 0.75 * left_hip_dist or right_knee_dist < 0.75 * right_hip_dist:
                    caved_frames += 1
                    
        if total_frames > 0:
            # If caving in for more than 15% of frames in rep, trigger violation
            return (caved_frames / total_frames) > 0.15
        return False
