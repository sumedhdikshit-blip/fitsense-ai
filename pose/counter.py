import time

class RepCounter:
    def __init__(self, exercise_key, exercise_config):
        self.exercise_key = exercise_key
        self.config = exercise_config
        
        self.primary_angle = self.config["primary_angle"]
        self.down_threshold = self.config["down_threshold"]
        self.up_threshold = self.config["up_threshold"]
        
        self.mode = self.config.get("mode", "rep")
        self.reps_counted = 0
        self.stage = None  # Will be initialized on first update
        
        self.all_rep_scores = []
        self.avg_form_score = 100.0
        self.latest_feedback = [{"message": "Get ready!", "severity": "GREEN"}]
        
        # Rep-specific tracking
        self.rep_min_angles = {}
        self.rep_max_angles = {}
        self.rep_landmarks = []
        
        # Isometric hold specific tracking
        self.last_update_time = None
        self.total_hold_time = 0.0
        self.good_form_time = 0.0

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
        Returns True if a new rep was completed (only applicable in rep mode).
        """
        if not current_angles or self.primary_angle not in current_angles:
            # Prevent time accumulation if tracking is lost
            self.last_update_time = None
            return False
        
        angle = current_angles[self.primary_angle]
        
        # Initialize stage on first frame
        if self.stage is None:
            if self.mode == "hold":
                self.stage = "break"
            else:
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
            
        if self.mode == "hold":
            now = time.time()
            dt = 0.0
            if self.last_update_time is not None:
                dt = now - self.last_update_time
            self.last_update_time = now
            
            # Determine if current angle is within holding range
            min_thresh = min(self.down_threshold, self.up_threshold)
            max_thresh = max(self.down_threshold, self.up_threshold)
            in_threshold = (min_thresh <= angle <= max_thresh)
            
            # Evaluate rules for the current frame
            frame_score, feedback = self.evaluate_form_rules(current_angles)
            has_red_violation = any(fb["severity"] == "RED" for fb in feedback)
            
            if in_threshold and not has_red_violation:
                self.stage = "holding"
                self.good_form_time += dt
            else:
                self.stage = "break"
                
            self.total_hold_time += dt
            
            # Form score = % of hold time in correct alignment
            if self.total_hold_time > 0:
                self.avg_form_score = (self.good_form_time / self.total_hold_time) * 100.0
            else:
                self.avg_form_score = 100.0
                
            self.latest_feedback = feedback
            # Reuse reps_counted to store active hold time in seconds
            self.reps_counted = int(self.good_form_time)
            return False
            
        else:
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

    def evaluate_form_rules(self, current_angles=None):
        feedback = []
        score = 100
        is_hold = (current_angles is not None)
        
        form_rules = self.config.get("form_rules", [])
        for rule in form_rules:
            check_str = rule["check"]
            severity = rule["severity"]
            rule_name = rule["name"]
            
            triggered = False
            
            if check_str == "knee_alignment_x":
                triggered = self._check_knee_alignment(current_frame_only=is_hold)
                
            elif ":" in check_str:
                cond, thresh_val = check_str.split(":")
                val = float(thresh_val)
                
                # Resolve key
                if cond.startswith("primary_angle"):
                    angle_key = self.primary_angle
                else:
                    # Resolve from naming convention: e.g. back_angle_lt -> back
                    angle_key = cond.split("_angle_")[0]
                
                if is_hold:
                    cur_val = current_angles.get(angle_key)
                    if cur_val is not None:
                        if "_lt" in cond or "lt_at" in cond:
                            if cur_val < val:
                                triggered = True
                        elif "_gt" in cond or "gt_at" in cond:
                            if cur_val > val:
                                triggered = True
                else:
                    min_val = self.rep_min_angles.get(angle_key, 180.0)
                    max_val = self.rep_max_angles.get(angle_key, 0.0)
                    
                    if "lt_at_bottom" in cond:
                        if max_val < val:
                            triggered = True
                    elif "gt_at_bottom" in cond or "gt_at_top" in cond:
                        if min_val > val:
                            triggered = True
                    elif "_lt" in cond:
                        if min_val < val:
                            triggered = True
                    elif "_gt" in cond:
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

    def _check_knee_alignment(self, current_frame_only=False):
        """
        Check if knees cave in (knee_alignment_x) relative to hip width.
        """
        caved_frames = 0
        total_frames = 0
        
        frames_to_check = [self.rep_landmarks[-1]] if (current_frame_only and self.rep_landmarks) else self.rep_landmarks
        
        for lm in frames_to_check:
            if not lm:
                continue
            left_hip = lm.get("left_hip")
            right_hip = lm.get("right_hip")
            left_knee = lm.get("left_knee")
            right_knee = lm.get("right_knee")
            
            if left_hip and right_hip and left_knee and right_knee:
                total_frames += 1
                center_x = (left_hip[0] + right_hip[0]) / 2.0
                
                left_hip_dist = abs(left_hip[0] - center_x)
                left_knee_dist = abs(left_knee[0] - center_x)
                
                right_hip_dist = abs(right_hip[0] - center_x)
                right_knee_dist = abs(right_knee[0] - center_x)
                
                if left_knee_dist < 0.75 * left_hip_dist or right_knee_dist < 0.75 * right_hip_dist:
                    caved_frames += 1
                    
        if total_frames > 0:
            if current_frame_only:
                return caved_frames > 0
            return (caved_frames / total_frames) > 0.15
        return False
