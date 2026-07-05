EXERCISE_LIBRARY = {
    'arm_circle': {
        'display_name': 'Arm Circles',
        'category': 'flexibility',
        'met_value': 2.2,
        'mode': 'rep',
        'angles': {
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 40,
        'up_threshold': 150,
        'form_rules': [
            {'name': 'Circles too small', 'check': 'left_shoulder_angle_lt:55', 'severity': 'YELLOW'},
        ],
        'description': 'Rotate your arms in circular motions to warm up and stretch the shoulder joints.'
    },
    'arnold_press': {
        'display_name': 'Arnold Press',
        'category': 'upper_body',
        'met_value': 6.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 80,
        'up_threshold': 165,
        'form_rules': [
            {'name': 'Incomplete overhead press', 'check': 'primary_angle_lt_at_bottom:150', 'severity': 'YELLOW'},
        ],
        'description': 'Clean a kettlebell to your shoulder. Clean the kettlebell to your shoulder by extending through the legs and hips as you raise the kettlebell towards your shoulder. The palm should be facing inward. Looking straight ahead, press the kettlebell out and overhead, rotating your wrist so that your palm faces forward at the top of the motion.'
    },
    'back_extension': {
        'display_name': 'Hyperextensions',
        'category': 'upper_body',
        'met_value': 3.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'back',
        'down_threshold': 180,
        'up_threshold': 140,
        'form_rules': [
            {'name': 'Hyperextension', 'check': 'back_angle_lt:130', 'severity': 'YELLOW'},
        ],
        'description': 'Lie face down on a hyperextension bench, tucking your ankles securely under the footpads. Adjust the upper pad if possible so your upper thighs lie flat across the wide pad, leaving enough room for you to bend at the waist without any restriction.'
    },
    'barbell_bench_press': {
        'display_name': 'Barbell Bench Press',
        'category': 'upper_body',
        'met_value': 6.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 80,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Incomplete contraction', 'check': 'primary_angle_gt_at_top:150', 'severity': 'YELLOW'},
            {'name': 'Bounce off chest', 'check': 'primary_angle_lt_at_bottom:85', 'severity': 'YELLOW'},
        ],
        'description': 'Lie back on a flat bench. Using a medium width grip (a grip that creates a 90-degree angle in the middle of the movement between the forearms and the upper arms), lift the bar from the rack and hold it straight over you with your arms locked. This will be your starting position. From the starting position, breathe in and begin coming down slowly until the bar touches your middle chest.'
    },
    'barbell_curl': {
        'display_name': 'Barbell Curl',
        'category': 'upper_body',
        'met_value': 4.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 40,
        'form_rules': [
            {'name': 'Swinging back', 'check': 'back_angle_lt:160', 'severity': 'RED'},
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:130', 'severity': 'YELLOW'},
        ],
        'description': 'Stand up with your torso upright while holding a barbell at a shoulder-width grip. The palm of your hands should be facing forward and the elbows should be close to the torso. This will be your starting position. While holding the upper arms stationary, curl the weights forward while contracting the biceps as you breathe out. Tip: Only the forearms should move.'
    },
    'barbell_overhead_press': {
        'display_name': 'Barbell Overhead Press',
        'category': 'upper_body',
        'met_value': 6.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 80,
        'up_threshold': 165,
        'form_rules': [
            {'name': 'Incomplete lock out', 'check': 'primary_angle_lt_at_bottom:150', 'severity': 'YELLOW'},
            {'name': 'Excessive arch in back', 'check': 'back_angle_lt:150', 'severity': 'RED'},
        ],
        'description': 'Start by placing a barbell that is about chest high on a squat rack. Once you have selected the weights, grab the barbell using a pronated (palms facing forward) grip. Make sure to grip the bar wider than shoulder width apart from each other. Slightly bend the knees and place the barbell on your collar bone. Lift the barbell up keeping it lying on your chest. Take a step back and position your feet shoulder width apart from each other.'
    },
    'bear_crawl': {
        'display_name': 'Bear Crawl',
        'category': 'cardio',
        'met_value': 8.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
        },
        'primary_angle': 'left_knee',
        'down_threshold': 95,
        'up_threshold': 140,
        'form_rules': [
            {'name': 'High hips', 'check': 'back_angle_gt:190', 'severity': 'YELLOW'},
        ],
        'description': 'Move on all fours close to the ground, keeping your knees bent and hips low.'
    },
    'bench_dip': {
        'display_name': 'Bench Dips',
        'category': 'upper_body',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 95,
        'up_threshold': 155,
        'form_rules': [
            {'name': 'Incomplete lockout', 'check': 'primary_angle_lt_at_bottom:140', 'severity': 'YELLOW'},
        ],
        'description': 'For this exercise you will need to place a bench behind your back. With the bench perpendicular to your body, and while looking away from it, hold on to the bench on its edge with the hands fully extended, separated at shoulder width. The legs will be extended forward, bent at the waist and perpendicular to your torso. This will be your starting position. Slowly lower your body as you inhale by bending at the elbows until you lower yourself far enough to where there is an angle slightly smaller than 90 degrees between the upper arm and the forearm. Tip: Keep the elbows as close as possible throughout the movement. Forearms should always be pointing down.'
    },
    'bent_over_lateral_raise': {
        'display_name': 'Bent-Over Lateral Raise',
        'category': 'upper_body',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 30,
        'up_threshold': 95,
        'form_rules': [
            {'name': 'Swinging torso', 'check': 'left_elbow_angle_lt:145', 'severity': 'YELLOW'},
        ],
        'description': 'Stand up straight while holding a dumbbell in each hand and with an incline bench in front of you. While keeping your back straight and maintaining the natural arch of your back, lean forward until your forehead touches the bench in front of you. Let the arms hang in front of you perpendicular to the ground. The palms of your hands should be facing each other and your torso should be parallel to the floor. This will be your starting position.'
    },
    'bent_over_row': {
        'display_name': 'Bent Over Barbell Row',
        'category': 'upper_body',
        'met_value': 6.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 75,
        'form_rules': [
            {'name': 'Leaning too high', 'check': 'back_angle_gt:160', 'severity': 'YELLOW'},
            {'name': 'Rounded back', 'check': 'back_angle_lt:140', 'severity': 'RED'},
        ],
        'description': 'Holding a barbell with a pronated grip (palms facing down), bend your knees slightly and bring your torso forward, by bending at the waist, while keeping the back straight until it is almost parallel to the floor. Tip: Make sure that you keep the head up. The barbell should hang directly in front of you as your arms hang perpendicular to the floor and your torso. This is your starting position. Now, while keeping the torso stationary, breathe out and lift the barbell to you. Keep the elbows close to the body and only use the forearms to hold the weight. At the top contracted position, squeeze the back muscles and hold for a brief pause.'
    },
    'bicep_curl': {
        'display_name': 'Bicep Curl',
        'category': 'upper_body',
        'met_value': 3.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 40,
        'form_rules': [
            {'name': 'Incomplete curl', 'check': 'primary_angle_gt_at_top:60', 'severity': 'YELLOW'},
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:130', 'severity': 'YELLOW'},
            {'name': 'Swinging back', 'check': 'back_angle_lt:160', 'severity': 'RED'},
        ],
        'description': 'Curl weights toward your shoulders by flexing your elbows while keeping upper arms stationary.'
    },
    'bicycle_crunch': {
        'display_name': 'Bicycle Crunch',
        'category': 'core',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
        },
        'primary_angle': 'left_knee',
        'down_threshold': 80,
        'up_threshold': 150,
        'form_rules': [
            {'name': 'Knees not moving', 'check': 'left_knee_angle_lt:60', 'severity': 'YELLOW'},
        ],
        'description': 'Perform a crunch while bringing opposite elbow to opposite knee in a pedaling motion.'
    },
    'bulgarian_split_squat': {
        'display_name': 'Bulgarian Split Squat',
        'category': 'lower_body',
        'met_value': 5.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
        },
        'primary_angle': 'left_knee',
        'down_threshold': 90,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Not deep enough', 'check': 'primary_angle_gt_at_bottom:110', 'severity': 'YELLOW'},
            {'name': 'Excessive forward lean', 'check': 'back_angle_lt:50', 'severity': 'YELLOW'},
        ],
        'description': 'Place one foot behind you on a bench and perform a split squat, targeting the front leg glutes and quads.'
    },
    'burpee': {
        'display_name': 'Burpee',
        'category': 'cardio',
        'met_value': 11.0,
        'mode': 'rep',
        'angles': {
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
        },
        'primary_angle': 'left_knee',
        'down_threshold': 95,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Not squatting deep', 'check': 'primary_angle_gt_at_bottom:115', 'severity': 'YELLOW'},
        ],
        'description': 'Perform a squat, drop to a plank, do a pushup, jump back to a squat, and jump vertically.'
    },
    'butt_kick': {
        'display_name': 'Butt Kickers',
        'category': 'cardio',
        'met_value': 8.0,
        'mode': 'rep',
        'angles': {
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
        },
        'primary_angle': 'left_knee',
        'down_threshold': 150,
        'up_threshold': 60,
        'form_rules': [
            {'name': 'Incomplete contraction', 'check': 'primary_angle_gt_at_top:85', 'severity': 'YELLOW'},
        ],
        'description': 'Run in place while bringing your heels up to touch your glutes.'
    },
    'cable_bicep_curl': {
        'display_name': 'Cable Bicep Curl',
        'category': 'upper_body',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 45,
        'form_rules': [
            {'name': 'Incomplete contraction', 'check': 'primary_angle_gt_at_top:70', 'severity': 'YELLOW'},
        ],
        'description': 'Stand between a couple of high pulleys and grab a handle in each arm. Position your upper arms in a way that they are parallel to the floor with the palms of your hands facing you. This will be your starting position. Curl the handles towards you until they are next to your ears. Make sure that as you do so you flex your biceps and exhale. The upper arms should remain stationary and only the forearms should move. Hold for a second in the contracted position as you squeeze the biceps.'
    },
    'cable_crossover': {
        'display_name': 'Cable Crossover',
        'category': 'upper_body',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 90,
        'up_threshold': 145,
        'form_rules': [
            {'name': 'Incomplete contraction', 'check': 'primary_angle_gt_at_top:130', 'severity': 'YELLOW'},
        ],
        'description': 'To get yourself into the starting position, place the pulleys on a high position (above your head), select the resistance to be used and hold the pulleys in each hand. Step forward in front of an imaginary straight line between both pulleys while pulling your arms together in front of you. Your torso should have a small forward bend from the waist. This will be your starting position.'
    },
    'cable_lateral_raise': {
        'display_name': 'Cable Lateral Raise',
        'category': 'upper_body',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 20,
        'up_threshold': 90,
        'form_rules': [
            {'name': 'Excessive body momentum', 'check': 'left_elbow_angle_lt:145', 'severity': 'YELLOW'},
        ],
        'description': 'Raise a low cable pulley laterally to shoulder height to maintain continuous resistance on the delts.'
    },
    'cable_overhead_extension': {
        'display_name': 'Cable Overhead Tricep Extension',
        'category': 'upper_body',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 80,
        'up_threshold': 155,
        'form_rules': [
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:140', 'severity': 'YELLOW'},
        ],
        'description': 'Attach a straight or angled bar to a high pulley and grab with an overhand grip (palms facing down) at shoulder width. Standing upright with the torso straight and a very small inclination forward, bring the upper arms close to your body and perpendicular to the floor. The forearms should be pointing up towards the pulley as they hold the bar. This is your starting position.'
    },
    'cable_pushdown': {
        'display_name': 'Triceps Pushdown',
        'category': 'upper_body',
        'met_value': 4.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 90,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Elbows flaring', 'check': 'primary_angle_lt_at_bottom:140', 'severity': 'YELLOW'},
        ],
        'description': 'Attach a straight or angled bar to a high pulley and grab with an overhand grip (palms facing down) at shoulder width. Standing upright with the torso straight and a very small inclination forward, bring the upper arms close to your body and perpendicular to the floor. The forearms should be pointing up towards the pulley as they hold the bar. This is your starting position.'
    },
    'calf_raise': {
        'display_name': 'Calf Raise',
        'category': 'lower_body',
        'met_value': 2.5,
        'mode': 'rep',
        'angles': {
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
        },
        'primary_angle': 'left_knee',
        'down_threshold': 170,
        'up_threshold': 180,
        'form_rules': [
            {'name': 'Knees bent', 'check': 'left_knee_angle_lt:160', 'severity': 'YELLOW'},
        ],
        'description': 'Rise up onto the balls of your feet from a standing position to contract the calf muscles.'
    },
    'cat_cow': {
        'display_name': 'Cat Cow Stretch',
        'category': 'flexibility',
        'met_value': 2.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
        },
        'primary_angle': 'back',
        'down_threshold': 170,
        'up_threshold': 150,
        'form_rules': [
            {'name': 'Insufficient arch', 'check': 'back_angle_gt:165', 'severity': 'YELLOW'},
        ],
        'description': 'Flow between arching your back upwards and arching it downwards on all fours to stretch the spine.'
    },
    'chest_dip': {
        'display_name': 'Chest Dip',
        'category': 'upper_body',
        'met_value': 6.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 80,
        'up_threshold': 155,
        'form_rules': [
            {'name': 'Not deep enough', 'check': 'primary_angle_gt_at_bottom:100', 'severity': 'YELLOW'},
        ],
        'description': 'Lean forward slightly on parallel bars and lower your body until elbows bend to 90 degrees, then push up.'
    },
    'chin_up': {
        'display_name': 'Chinups',
        'category': 'upper_body',
        'met_value': 7.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 65,
        'form_rules': [
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:130', 'severity': 'YELLOW'},
        ],
        'description': 'Grab the pull-up bar with the palms facing your torso and a grip closer than the shoulder width. As you have both arms extended in front of you holding the bar at the chosen grip width, keep your torso as straight as possible while creating a curvature on your lower back and sticking your chest out. This is your starting position. Tip: Keeping the torso as straight as possible maximizes biceps stimulation while minimizing back involvement.'
    },
    'close_grip_bench_press': {
        'display_name': 'Close-Grip Bench Press',
        'category': 'upper_body',
        'met_value': 6.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 85,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Incomplete lockout', 'check': 'primary_angle_lt_at_bottom:145', 'severity': 'YELLOW'},
        ],
        'description': 'Lie back on a flat bench. Using a close grip (around shoulder width), lift the bar from the rack and hold it straight over you with your arms locked. This will be your starting position. As you breathe in, come down slowly until you feel the bar on your middle chest. Tip: Make sure that - as opposed to a regular bench press - you keep the elbows close to the torso at all times in order to maximize triceps involvement.'
    },
    'cobra_stretch': {
        'display_name': 'Cobra Stretch',
        'category': 'flexibility',
        'met_value': 2.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
        },
        'primary_angle': 'back',
        'down_threshold': 170,
        'up_threshold': 145,
        'form_rules': [
            {'name': 'Insufficient extension', 'check': 'back_angle_gt:160', 'severity': 'YELLOW'},
        ],
        'description': 'Lie face down and press your upper body up using your arms to stretch the abdominals.'
    },
    'concentration_curl': {
        'display_name': 'Concentration Curls',
        'category': 'upper_body',
        'met_value': 3.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 45,
        'form_rules': [
            {'name': 'Incomplete range', 'check': 'primary_angle_gt_at_top:70', 'severity': 'YELLOW'},
        ],
        'description': 'Sit down on a flat bench with one dumbbell in front of you between your legs. Your legs should be spread with your knees bent and feet on the floor. Use your right arm to pick the dumbbell up. Place the back of your right upper arm on the top of your inner right thigh. Rotate the palm of your hand until it is facing forward away from your thigh. Tip: Your arm should be extended and the dumbbell should be above the floor. This will be your starting position.'
    },
    'conventional_deadlift': {
        'display_name': 'Conventional Deadlift',
        'category': 'lower_body',
        'met_value': 6.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'hip',
        'down_threshold': 110,
        'up_threshold': 170,
        'form_rules': [
            {'name': 'Rounded back', 'check': 'back_angle_lt:140', 'severity': 'RED'},
            {'name': 'Knees caving', 'check': 'knee_alignment_x', 'severity': 'YELLOW'},
        ],
        'description': 'Stand in front of a loaded barbell. While keeping the back as straight as possible, bend your knees, bend forward and grasp the bar using a medium (shoulder width) overhand grip. This will be the starting position of the exercise. Tip: If it is difficult to hold on to the bar with this grip, alternate your grip or use wrist straps.'
    },
    'crunch': {
        'display_name': 'Abdominal Crunch',
        'category': 'core',
        'met_value': 2.8,
        'mode': 'rep',
        'angles': {
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
        },
        'primary_angle': 'hip',
        'down_threshold': 140,
        'up_threshold': 110,
        'form_rules': [
            {'name': 'Insufficient flexion', 'check': 'primary_angle_gt_at_top:125', 'severity': 'YELLOW'},
        ],
        'description': 'Lie on your back and curl your shoulders towards your hips, contracting the abdominal muscles.'
    },
    'dead_bug': {
        'display_name': 'Dead Bug',
        'category': 'core',
        'met_value': 3.0,
        'mode': 'rep',
        'angles': {
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
        },
        'primary_angle': 'hip',
        'down_threshold': 160,
        'up_threshold': 100,
        'form_rules': [
            {'name': 'Knees not matching 90deg', 'check': 'primary_angle_gt_at_top:115', 'severity': 'YELLOW'},
        ],
        'description': 'Lie on your back and extend opposite arm and leg while keeping the lower back flat on the floor.'
    },
    'decline_barbell_bench_press': {
        'display_name': 'Decline Barbell Bench Press',
        'category': 'upper_body',
        'met_value': 6.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 80,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Incomplete lockout', 'check': 'primary_angle_lt_at_bottom:145', 'severity': 'YELLOW'},
        ],
        'description': 'Secure your legs at the end of the decline bench and slowly lay down on the bench. Using a medium width grip (a grip that creates a 90-degree angle in the middle of the movement between the forearms and the upper arms), lift the bar from the rack and hold it straight over you with your arms locked. The arms should be perpendicular to the floor. This will be your starting position. Tip: In order to protect your rotator cuff, it is best if you have a spotter help you lift the barbell off the rack.'
    },
    'decline_dumbbell_bench_press': {
        'display_name': 'Decline Dumbbell Bench Press',
        'category': 'upper_body',
        'met_value': 6.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 80,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Incomplete lockout', 'check': 'primary_angle_lt_at_bottom:145', 'severity': 'YELLOW'},
        ],
        'description': 'Secure your legs at the end of the decline bench and lie down with a dumbbell on each hand on top of your thighs. The palms of your hand will be facing each other. Once you are laying down, move the dumbbells in front of you at shoulder width.'
    },
    'decline_pushup': {
        'display_name': 'Decline Pushup',
        'category': 'upper_body',
        'met_value': 9.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 90,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Sagging hips', 'check': 'back_angle_lt:140', 'severity': 'RED'},
        ],
        'description': 'Perform a pushup with your feet placed on an elevated surface to target the upper chest.'
    },
    'diamond_pushup': {
        'display_name': 'Diamond Pushup',
        'category': 'upper_body',
        'met_value': 8.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 90,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Not deep enough', 'check': 'primary_angle_gt_at_bottom:115', 'severity': 'YELLOW'},
            {'name': 'Sagging hips', 'check': 'back_angle_lt:140', 'severity': 'RED'},
        ],
        'description': 'Perform a pushup with hands close together forming a diamond shape to emphasize the triceps.'
    },
    'doorway_row': {
        'display_name': 'Doorway Row',
        'category': 'upper_body',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 75,
        'form_rules': [
            {'name': 'Incomplete contraction', 'check': 'primary_angle_gt_at_top:90', 'severity': 'YELLOW'},
        ],
        'description': 'Hold onto a door frame and lean back, pulling your chest towards the frame using your back muscles.'
    },
    'dumbbell_bench_press': {
        'display_name': 'Dumbbell Bench Press',
        'category': 'upper_body',
        'met_value': 6.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 80,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:145', 'severity': 'YELLOW'},
        ],
        'description': 'Lie down on a flat bench with a dumbbell in each hand resting on top of your thighs. The palms of your hands will be facing each other. Then, using your thighs to help raise the dumbbells up, lift the dumbbells one at a time so that you can hold them in front of you at shoulder width.'
    },
    'dumbbell_fly': {
        'display_name': 'Dumbbell Flyes',
        'category': 'upper_body',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 90,
        'up_threshold': 150,
        'form_rules': [
            {'name': 'Elbows bent too much', 'check': 'left_elbow_angle_lt:110', 'severity': 'YELLOW'},
        ],
        'description': "Lie down on a flat bench with a dumbbell on each hand resting on top of your thighs. The palms of your hand will be facing each other. Then using your thighs to help raise the dumbbells, lift the dumbbells one at a time so you can hold them in front of you at shoulder width with the palms of your hands facing each other. Raise the dumbbells up like you're pressing them, but stop and hold just before you lock out. This will be your starting position."
    },
    'dumbbell_front_raise': {
        'display_name': 'Dumbbell Front Raise',
        'category': 'upper_body',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 25,
        'up_threshold': 90,
        'form_rules': [
            {'name': 'Bending elbows too much', 'check': 'left_elbow_angle_lt:145', 'severity': 'YELLOW'},
        ],
        'description': 'Pick a couple of dumbbells and stand with a straight torso and the dumbbells on front of your thighs at arms length with the palms of the hand facing your thighs. This will be your starting position. While maintaining the torso stationary (no swinging), lift the left dumbbell to the front with a slight bend on the elbow and the palms of the hands always facing down. Continue to go up until you arm is slightly above parallel to the floor. Exhale as you execute this portion of the movement and pause for a second at the top. Inhale after the second pause.'
    },
    'dumbbell_kickback': {
        'display_name': 'Tricep Dumbbell Kickback',
        'category': 'upper_body',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 90,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Dropping elbow', 'check': 'primary_angle_lt_at_bottom:140', 'severity': 'YELLOW'},
        ],
        'description': 'Start with a dumbbell in each hand and your palms facing your torso. Keep your back straight with a slight bend in the knees and bend forward at the waist. Your torso should be almost parallel to the floor. Make sure to keep your head up. Your upper arms should be close to your torso and parallel to the floor. Your forearms should be pointed towards the floor as you hold the weights. There should be a 90-degree angle formed between your forearm and upper arm. This is your starting position. Now, while keeping your upper arms stationary, exhale and use your triceps to lift the weights until the arm is fully extended. Focus on moving the forearm.'
    },
    'dumbbell_lateral_raise': {
        'display_name': 'Dumbbell Lateral Raise',
        'category': 'upper_body',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 25,
        'up_threshold': 90,
        'form_rules': [
            {'name': 'Raising too high', 'check': 'primary_angle_gt:105', 'severity': 'YELLOW'},
            {'name': 'Bent elbows', 'check': 'left_elbow_angle_lt:145', 'severity': 'YELLOW'},
        ],
        'description': 'Stand in the middle of two low pulleys that are opposite to each other and place a flat bench right behind you (in perpendicular fashion to you; the narrow edge of the bench should be the one behind you). Select the weight to be used on each pulley. Now sit at the edge of the flat bench behind you with your feet placed in front of your knees.'
    },
    'face_pull': {
        'display_name': 'Face Pull',
        'category': 'upper_body',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 145,
        'up_threshold': 80,
        'form_rules': [
            {'name': 'Pulling too low', 'check': 'primary_angle_gt_at_top:95', 'severity': 'YELLOW'},
        ],
        'description': 'Facing a high pulley with a rope or dual handles attached, pull the weight directly towards your face, separating your hands as you do so. Keep your upper arms parallel to the ground.'
    },
    'flutter_kick': {
        'display_name': 'Flutter Kick',
        'category': 'core',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
        },
        'primary_angle': 'hip',
        'down_threshold': 165,
        'up_threshold': 140,
        'form_rules': [
            {'name': 'Lifting legs too high', 'check': 'hip_angle_lt:130', 'severity': 'YELLOW'},
        ],
        'description': 'Lie on your back and raise your legs slightly, kicking them up and down in a quick motion.'
    },
    'glute_bridge': {
        'display_name': 'Glute Bridge',
        'category': 'lower_body',
        'met_value': 3.0,
        'mode': 'rep',
        'angles': {
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
        },
        'primary_angle': 'hip',
        'down_threshold': 120,
        'up_threshold': 165,
        'form_rules': [
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:150', 'severity': 'YELLOW'},
        ],
        'description': 'Lie on your back with knees bent and lift your hips toward the ceiling, contracting your glutes.'
    },
    'hammer_curl': {
        'display_name': 'Hammer Curl',
        'category': 'upper_body',
        'met_value': 3.0,
        'mode': 'rep',
        'angles': {
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 45,
        'form_rules': [
            {'name': 'Incomplete curl', 'check': 'primary_angle_gt_at_top:65', 'severity': 'YELLOW'},
        ],
        'description': 'Perform a bicep curl with a neutral grip (palms facing each other) to target the brachialis.'
    },
    'high_knees': {
        'display_name': 'High Knees',
        'category': 'cardio',
        'met_value': 9.0,
        'mode': 'rep',
        'angles': {
            'left_hip_angle': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
        },
        'primary_angle': 'left_knee',
        'down_threshold': 80,
        'up_threshold': 150,
        'form_rules': [
            {'name': 'Knees too low', 'check': 'left_knee_angle_gt_at_bottom:100', 'severity': 'YELLOW'},
        ],
        'description': 'Run in place while driving your knees up to hip height to build cardiovascular endurance.'
    },
    'hip_circle': {
        'display_name': 'Hip Circles',
        'category': 'flexibility',
        'met_value': 2.5,
        'mode': 'rep',
        'angles': {
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
        },
        'primary_angle': 'hip',
        'down_threshold': 170,
        'up_threshold': 155,
        'form_rules': [
            {'name': 'Stiff hips', 'check': 'hip_angle_gt:168', 'severity': 'YELLOW'},
        ],
        'description': 'Rotate your hips in circular motions to improve mobility in the hip joints.'
    },
    'hollow_hold': {
        'display_name': 'Hollow Body Hold',
        'category': 'core',
        'met_value': 3.5,
        'mode': 'hold',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
        },
        'primary_angle': 'hip',
        'down_threshold': 110,
        'up_threshold': 150,
        'form_rules': [
            {'name': 'Back arching', 'check': 'back_angle_gt:165', 'severity': 'RED'},
        ],
        'description': 'Lie on your back and raise legs and shoulders slightly off the ground, forming a hollow shape.'
    },
    'incline_barbell_bench_press': {
        'display_name': 'Incline Barbell Bench Press',
        'category': 'upper_body',
        'met_value': 6.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 85,
        'up_threshold': 155,
        'form_rules': [
            {'name': 'Bar too high on chest', 'check': 'left_elbow_angle_lt:90', 'severity': 'YELLOW'},
        ],
        'description': 'Lie on an incline bench and press a barbell from your upper chest to full elbow extension overhead.'
    },
    'incline_dumbbell_bench_press': {
        'display_name': 'Incline Dumbbell Bench Press',
        'category': 'upper_body',
        'met_value': 6.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 85,
        'up_threshold': 155,
        'form_rules': [
            {'name': 'Incomplete range', 'check': 'primary_angle_gt_at_bottom:100', 'severity': 'YELLOW'},
        ],
        'description': 'Lie down on a flat bench with a dumbbell in each hand resting on top of your thighs. The palms of your hands will be facing each other. Then, using your thighs to help raise the dumbbells up, lift the dumbbells one at a time so that you can hold them in front of you at shoulder width.'
    },
    'incline_dumbbell_curl': {
        'display_name': 'Incline Dumbbell Curl',
        'category': 'upper_body',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 155,
        'up_threshold': 45,
        'form_rules': [
            {'name': 'Shoulders drifting', 'check': 'primary_angle_lt_at_bottom:135', 'severity': 'YELLOW'},
        ],
        'description': 'Sit back on an incline bench with a dumbbell in each hand held at arms length. Keep your elbows close to your torso and rotate the palms of your hands until they are facing forward. This will be your starting position. While holding the upper arm stationary, curl the weights forward while contracting the biceps as you breathe out. Only the forearms should move. Continue the movement until your biceps are fully contracted and the dumbbells are at shoulder level. Hold the contracted position for a second.'
    },
    'incline_dumbbell_fly': {
        'display_name': 'Incline Dumbbell Fly',
        'category': 'upper_body',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 95,
        'up_threshold': 145,
        'form_rules': [
            {'name': 'Arms bent too much', 'check': 'left_elbow_angle_lt:115', 'severity': 'YELLOW'},
        ],
        'description': 'Hold a dumbbell on each hand and lie on an incline bench that is set to an incline angle of no more than 30 degrees. Extend your arms above you with a slight bend at the elbows.'
    },
    'incline_hammer_curl': {
        'display_name': 'Incline Hammer Curl',
        'category': 'upper_body',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 45,
        'form_rules': [
            {'name': 'Elbow drift', 'check': 'primary_angle_lt_at_bottom:130', 'severity': 'YELLOW'},
        ],
        'description': 'Seat yourself on an incline bench with a dumbbell in each hand. You should pressed firmly against he back with your feet together. Allow the dumbbells to hang straight down at your side, holding them with a neutral grip. This will be your starting position. Initiate the movement by flexing at the elbow, attempting to keep the upper arm stationary.'
    },
    'incline_pushup': {
        'display_name': 'Incline Pushup',
        'category': 'upper_body',
        'met_value': 6.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 90,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Not deep enough', 'check': 'primary_angle_gt_at_bottom:110', 'severity': 'YELLOW'},
        ],
        'description': 'Perform a pushup with your hands placed on an elevated surface to target the lower chest.'
    },
    'inverted_row': {
        'display_name': 'Inverted Row',
        'category': 'upper_body',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 75,
        'form_rules': [
            {'name': 'Hips sagging', 'check': 'back_angle_lt:145', 'severity': 'RED'},
        ],
        'description': 'Position a bar in a rack to about waist height. You can also use a smith machine. Take a wider than shoulder width grip on the bar and position yourself hanging underneath the bar. Your body should be straight with your heels on the ground with your arms fully extended. This will be your starting position.'
    },
    'jump_rope': {
        'display_name': 'Jump Rope Simulation',
        'category': 'cardio',
        'met_value': 12.0,
        'mode': 'rep',
        'angles': {
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
        },
        'primary_angle': 'left_knee',
        'down_threshold': 155,
        'up_threshold': 175,
        'form_rules': [
            {'name': 'Bending knees too much', 'check': 'left_knee_angle_lt:145', 'severity': 'YELLOW'},
        ],
        'description': 'Simulate jumping rope in place with small jumps and circular wrist movements.'
    },
    'jump_squat': {
        'display_name': 'Jump Squat',
        'category': 'lower_body',
        'met_value': 8.0,
        'mode': 'rep',
        'angles': {
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
        },
        'primary_angle': 'left_knee',
        'down_threshold': 100,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Not deep enough', 'check': 'primary_angle_gt_at_bottom:120', 'severity': 'YELLOW'},
        ],
        'description': 'Perform a standard squat and explosively jump vertically at the top of the movement.'
    },
    'jumping_jack': {
        'display_name': 'Jumping Jack',
        'category': 'cardio',
        'met_value': 8.0,
        'mode': 'rep',
        'angles': {
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 30,
        'up_threshold': 130,
        'form_rules': [
            {'name': 'Low arm raises', 'check': 'primary_angle_gt_at_bottom:90', 'severity': 'YELLOW'},
        ],
        'description': 'Jump to a wide stance while raising arms overhead, then return to the starting position.'
    },
    'lat_pulldown': {
        'display_name': 'Wide-Grip Lat Pulldown',
        'category': 'upper_body',
        'met_value': 4.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 70,
        'form_rules': [
            {'name': 'Incomplete pulldown', 'check': 'primary_angle_gt_at_top:90', 'severity': 'YELLOW'},
            {'name': 'Leaning back too much', 'check': 'back_angle_lt:135', 'severity': 'YELLOW'},
        ],
        'description': 'Sit down on a pull-down machine with a wide bar attached to the top pulley. Make sure that you adjust the knee pad of the machine to fit your height. These pads will prevent your body from being raised by the resistance attached to the bar. Grab the bar with the palms facing forward using the prescribed grip. Note on grips: For a wide grip, your hands need to be spaced out at a distance wider than shoulder width. For a medium grip, your hands need to be spaced out at a distance equal to your shoulder width and for a close grip at a distance smaller than your shoulder width.'
    },
    'leg_raise': {
        'display_name': 'Leg Raise',
        'category': 'core',
        'met_value': 3.0,
        'mode': 'rep',
        'angles': {
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
        },
        'primary_angle': 'hip',
        'down_threshold': 170,
        'up_threshold': 100,
        'form_rules': [
            {'name': 'Bending knees', 'check': 'primary_angle_gt_at_top:115', 'severity': 'YELLOW'},
        ],
        'description': 'Lie on your back and raise your legs to vertical, keeping them straight to target the lower abs.'
    },
    'lunge': {
        'display_name': 'Lunge',
        'category': 'lower_body',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
        },
        'primary_angle': 'left_knee',
        'down_threshold': 95,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Knees caving in', 'check': 'knee_alignment_x', 'severity': 'YELLOW'},
            {'name': 'Not deep enough', 'check': 'primary_angle_gt_at_bottom:110', 'severity': 'YELLOW'},
        ],
        'description': 'Step forward with one leg, bending both knees to 90 degrees while keeping your torso upright.'
    },
    'mountain_climber': {
        'display_name': 'Mountain Climber',
        'category': 'core',
        'met_value': 8.0,
        'mode': 'rep',
        'angles': {
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
        },
        'primary_angle': 'left_knee',
        'down_threshold': 70,
        'up_threshold': 150,
        'form_rules': [
            {'name': 'Hips raised too high', 'check': 'left_knee_angle_gt:165', 'severity': 'YELLOW'},
        ],
        'description': 'Drive your knees alternately toward your chest from a pushup position.'
    },
    'one_arm_dumbbell_row': {
        'display_name': 'One-Arm Dumbbell Row',
        'category': 'upper_body',
        'met_value': 5.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 155,
        'up_threshold': 75,
        'form_rules': [
            {'name': 'Rounded back', 'check': 'back_angle_lt:145', 'severity': 'RED'},
        ],
        'description': 'Choose a flat bench and place a dumbbell on each side of it. Place the right leg on top of the end of the bench, bend your torso forward from the waist until your upper body is parallel to the floor, and place your right hand on the other end of the bench for support.'
    },
    'overhead_dumbbell_extension': {
        'display_name': 'Overhead Dumbbell Extension',
        'category': 'upper_body',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 80,
        'up_threshold': 155,
        'form_rules': [
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:140', 'severity': 'YELLOW'},
        ],
        'description': 'Hold a dumbbell overhead with both hands, lower it behind your neck, and extend elbows back up.'
    },
    'pike_pushup': {
        'display_name': 'Pike Pushup',
        'category': 'upper_body',
        'met_value': 8.0,
        'mode': 'rep',
        'angles': {
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 95,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Not deep enough', 'check': 'primary_angle_gt_at_bottom:115', 'severity': 'YELLOW'},
        ],
        'description': 'Perform a pushup with hips raised high in a V-position to target the shoulders.'
    },
    'plank': {
        'display_name': 'Forearm Plank',
        'category': 'core',
        'met_value': 3.0,
        'mode': 'hold',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 70,
        'up_threshold': 110,
        'form_rules': [
            {'name': 'Sagging hips', 'check': 'back_angle_lt:140', 'severity': 'RED'},
            {'name': 'High hips', 'check': 'back_angle_gt:200', 'severity': 'RED'},
        ],
        'description': 'Hold a straight body position supported by your forearms and toes to build core stability.'
    },
    'preacher_curl': {
        'display_name': 'Preacher Curl',
        'category': 'upper_body',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 145,
        'up_threshold': 45,
        'form_rules': [
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:125', 'severity': 'YELLOW'},
        ],
        'description': 'To perform this movement you will need a preacher bench and an E-Z bar. Grab the E-Z curl bar at the close inner handle (either have someone hand you the bar which is preferable or grab the bar from the front bar rest provided by most preacher benches). The palm of your hands should be facing forward and they should be slightly tilted inwards due to the shape of the bar. With the upper arms positioned against the preacher bench pad and the chest against it, hold the E-Z Curl Bar at shoulder length. This will be your starting position.'
    },
    'pull_up': {
        'display_name': 'Pullups',
        'category': 'upper_body',
        'met_value': 8.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 70,
        'form_rules': [
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:130', 'severity': 'YELLOW'},
            {'name': 'Kipping/Swinging', 'check': 'back_angle_lt:155', 'severity': 'YELLOW'},
        ],
        'description': 'Grab the pull-up bar with the palms facing forward using the prescribed grip. Note on grips: For a wide grip, your hands need to be spaced out at a distance wider than your shoulder width. For a medium grip, your hands need to be spaced out at a distance equal to your shoulder width and for a close grip at a distance smaller than your shoulder width. As you have both arms extended in front of you holding the bar at the chosen grip width, bring your torso back around 30 degrees or so while creating a curvature on your lower back and sticking your chest out. This is your starting position.'
    },
    'pushup': {
        'display_name': 'Pushup',
        'category': 'upper_body',
        'met_value': 8.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 90,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Not deep enough', 'check': 'primary_angle_gt_at_bottom:110', 'severity': 'YELLOW'},
            {'name': 'Sagging hips', 'check': 'back_angle_lt:140', 'severity': 'RED'},
            {'name': 'High hips', 'check': 'back_angle_gt:190', 'severity': 'YELLOW'},
        ],
        'description': 'Lower your body to the ground using your arms and push back up while keeping a rigid plank position.'
    },
    'resistance_band_row': {
        'display_name': 'Resistance Band Row',
        'category': 'upper_body',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 80,
        'form_rules': [
            {'name': 'Hunching back', 'check': 'back_angle_lt:150', 'severity': 'RED'},
        ],
        'description': 'Pull a resistance band toward your torso while keeping your back straight and chest up.'
    },
    'reverse_barbell_curl': {
        'display_name': 'Reverse Barbell Curl',
        'category': 'upper_body',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 50,
        'form_rules': [
            {'name': 'Swinging torso', 'check': 'back_angle_lt:160', 'severity': 'RED'},
        ],
        'description': 'Stand up with your torso upright while holding a barbell at shoulder width with the elbows close to the torso. The palm of your hands should be facing down (pronated grip). This will be your starting position. While holding the upper arms stationary, curl the weights while contracting the biceps as you breathe out. Only the forearms should move. Continue the movement until your biceps are fully contracted and the bar is at shoulder level. Hold the contracted position for a second as you squeeze the muscle.'
    },
    'reverse_fly': {
        'display_name': 'Reverse Fly',
        'category': 'upper_body',
        'met_value': 3.0,
        'mode': 'rep',
        'angles': {
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 160,
        'up_threshold': 120,
        'form_rules': [
            {'name': 'Elbows bent too much', 'check': 'left_elbow_angle_lt:110', 'severity': 'YELLOW'},
        ],
        'description': 'Raise dumbbells out to the sides while bent forward at the hips to target the posterior deltoids.'
    },
    'romanian_deadlift': {
        'display_name': 'Romanian Deadlift',
        'category': 'lower_body',
        'met_value': 5.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'hip',
        'down_threshold': 120,
        'up_threshold': 170,
        'form_rules': [
            {'name': 'Rounded back', 'check': 'back_angle_lt:140', 'severity': 'RED'},
            {'name': 'Bending knees too much', 'check': 'left_knee_angle_lt:135', 'severity': 'YELLOW'},
        ],
        'description': 'Put a barbell in front of you on the ground and grab it using a pronated (palms facing down) grip that a little wider than shoulder width. Tip: Depending on the weight used, you may need wrist wraps to perform the exercise and also a raised platform in order to allow for better range of motion. Bend the knees slightly and keep the shins vertical, hips back and back straight. This will be your starting position.'
    },
    'russian_twist': {
        'display_name': 'Russian Twist',
        'category': 'core',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
        },
        'primary_angle': 'hip',
        'down_threshold': 130,
        'up_threshold': 95,
        'form_rules': [
            {'name': 'Slouching back', 'check': 'hip_angle_gt:135', 'severity': 'YELLOW'},
        ],
        'description': 'Sit with knees bent, lean back slightly, and rotate your torso from side to side.'
    },
    'seated_cable_row': {
        'display_name': 'Seated Cable Row',
        'category': 'upper_body',
        'met_value': 4.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 80,
        'form_rules': [
            {'name': 'Leaning back too much', 'check': 'back_angle_lt:135', 'severity': 'YELLOW'},
            {'name': 'Hunching back', 'check': 'back_angle_lt:145', 'severity': 'RED'},
        ],
        'description': 'For this exercise you will need access to a low pulley row machine with a V-bar. Note: The V-bar will enable you to have a neutral grip where the palms of your hands face each other. To get into the starting position, first sit down on the machine and place your feet on the front platform or crossbar provided making sure that your knees are slightly bent and not locked. Lean over as you keep the natural alignment of your back and grab the V-bar handles.'
    },
    'shadow_boxing': {
        'display_name': 'Shadow Boxing',
        'category': 'cardio',
        'met_value': 5.5,
        'mode': 'rep',
        'angles': {
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 80,
        'up_threshold': 150,
        'form_rules': [
            {'name': 'Lazy punches', 'check': 'left_elbow_angle_lt:100', 'severity': 'YELLOW'},
        ],
        'description': 'Perform punches and footwork in the air to train speed, endurance, and coordination.'
    },
    'shoulder_press': {
        'display_name': 'Shoulder Press',
        'category': 'upper_body',
        'met_value': 6.0,
        'mode': 'rep',
        'angles': {
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 80,
        'up_threshold': 165,
        'form_rules': [
            {'name': 'Incomplete overhead extension', 'check': 'primary_angle_lt_at_bottom:150', 'severity': 'YELLOW'},
        ],
        'description': 'Press weights vertically overhead from shoulder height to full elbow extension.'
    },
    'side_plank': {
        'display_name': 'Side Plank',
        'category': 'core',
        'met_value': 3.0,
        'mode': 'hold',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 70,
        'up_threshold': 110,
        'form_rules': [
            {'name': 'Sagging hips', 'check': 'back_angle_lt:130', 'severity': 'RED'},
        ],
        'description': 'Support your body weight on one forearm and the side of one foot to target the obliques.'
    },
    'single_leg_deadlift': {
        'display_name': 'Single Leg Deadlift',
        'category': 'lower_body',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
        },
        'primary_angle': 'hip',
        'down_threshold': 110,
        'up_threshold': 170,
        'form_rules': [
            {'name': 'Rounded back', 'check': 'back_angle_lt:145', 'severity': 'RED'},
        ],
        'description': 'Hinge forward at the hips on one leg while extending the other leg straight behind you.'
    },
    'skater_hop': {
        'display_name': 'Skater Hops',
        'category': 'cardio',
        'met_value': 8.0,
        'mode': 'rep',
        'angles': {
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
        },
        'primary_angle': 'left_knee',
        'down_threshold': 120,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Hops too shallow', 'check': 'primary_angle_gt_at_bottom:140', 'severity': 'YELLOW'},
        ],
        'description': 'Leap laterally from side to side, landing on one foot while keeping the other foot behind you.'
    },
    'skull_crusher': {
        'display_name': 'Lying Triceps Press',
        'category': 'upper_body',
        'met_value': 5.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 85,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Elbows drifting forward', 'check': 'primary_angle_lt_at_bottom:140', 'severity': 'YELLOW'},
        ],
        'description': 'Lie on a flat bench with either an e-z bar (my preference) or a straight bar placed on the floor behind your head and your feet on the floor. Grab the bar behind you, using a medium overhand (pronated) grip, and raise the bar in front of you at arms length. Tip: The arms should be perpendicular to the torso and the floor. The elbows should be tucked in. This is the starting position.'
    },
    'spider_curl': {
        'display_name': 'Spider Curl',
        'category': 'upper_body',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 45,
        'form_rules': [
            {'name': 'Swinging arms', 'check': 'primary_angle_lt_at_bottom:135', 'severity': 'YELLOW'},
        ],
        'description': 'Start out by setting the bar on the part of the preacher bench that you would normally sit on. Make sure to align the barbell properly so that it is balanced and will not fall off. Move to the front side of the preacher bench (the part where the arms usually lay) and position yourself to lay at a 45 degree slant with your torso and stomach pressed against the front side of the preacher bench.'
    },
    'squat': {
        'display_name': 'Squat',
        'category': 'lower_body',
        'met_value': 5.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
        },
        'primary_angle': 'left_knee',
        'down_threshold': 90,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Knees caving in', 'check': 'knee_alignment_x', 'severity': 'RED'},
            {'name': 'Not deep enough', 'check': 'primary_angle_gt_at_bottom:110', 'severity': 'YELLOW'},
            {'name': 'Forward lean', 'check': 'back_angle_lt:45', 'severity': 'YELLOW'},
        ],
        'description': 'Lower your hips from a standing position and stand back up, keeping your knees aligned and back straight.'
    },
    'squat_jump_tuck': {
        'display_name': 'Tuck Jump',
        'category': 'cardio',
        'met_value': 12.5,
        'mode': 'rep',
        'angles': {
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
        },
        'primary_angle': 'left_knee',
        'down_threshold': 90,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Low tuck', 'check': 'primary_angle_gt_at_bottom:110', 'severity': 'YELLOW'},
        ],
        'description': 'Perform a squat jump and tuck your knees toward your chest at the peak of the jump.'
    },
    'standing_side_bend': {
        'display_name': 'Standing Side Bend',
        'category': 'flexibility',
        'met_value': 2.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
        },
        'primary_angle': 'back',
        'down_threshold': 170,
        'up_threshold': 150,
        'form_rules': [
            {'name': 'Too fast', 'check': 'back_angle_gt:165', 'severity': 'YELLOW'},
        ],
        'description': 'Reach one arm overhead and lean to the opposite side from a standing position.'
    },
    'star_jump': {
        'display_name': 'Star Jump',
        'category': 'cardio',
        'met_value': 10.0,
        'mode': 'rep',
        'angles': {
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 30,
        'up_threshold': 140,
        'form_rules': [
            {'name': 'Low jumps', 'check': 'primary_angle_gt_at_bottom:95', 'severity': 'YELLOW'},
        ],
        'description': 'Squat down and explosively jump, extending arms and legs outwards in a star shape.'
    },
    'step_up': {
        'display_name': 'Step Up',
        'category': 'lower_body',
        'met_value': 4.5,
        'mode': 'rep',
        'angles': {
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
        },
        'primary_angle': 'left_knee',
        'down_threshold': 95,
        'up_threshold': 170,
        'form_rules': [
            {'name': 'Incomplete hip extension', 'check': 'primary_angle_lt_at_bottom:155', 'severity': 'YELLOW'},
        ],
        'description': 'Step onto an elevated platform with one leg and drive your body upward to full hip extension.'
    },
    'straight_arm_pulldown': {
        'display_name': 'Straight-Arm Pulldown',
        'category': 'upper_body',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 40,
        'up_threshold': 110,
        'form_rules': [
            {'name': 'Bending elbows too much', 'check': 'left_elbow_angle_lt:130', 'severity': 'YELLOW'},
        ],
        'description': 'You will start by grabbing the wide bar from the top pulley of a pulldown machine and using a wider than shoulder-width pronated (palms down) grip. Step backwards two feet or so. Bend your torso forward at the waist by around 30-degrees with your arms fully extended in front of you and a slight bend at the elbows. If your arms are not fully extended then you need to step a bit more backwards until they are. Once your arms are fully extended and your torso is slightly bent at the waist, tighten the lats and then you are ready to begin.'
    },
    'sumo_deadlift': {
        'display_name': 'Sumo Deadlift',
        'category': 'lower_body',
        'met_value': 6.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_knee',
        'down_threshold': 100,
        'up_threshold': 165,
        'form_rules': [
            {'name': 'Rounded back', 'check': 'back_angle_lt:140', 'severity': 'RED'},
            {'name': 'Knees caving in', 'check': 'knee_alignment_x', 'severity': 'RED'},
        ],
        'description': 'Begin with a bar loaded on the ground. Approach the bar so that the bar intersects the middle of the feet. The feet should be set very wide, near the collars. Bend at the hips to grip the bar. The arms should be directly below the shoulders, inside the legs, and you can use a pronated grip, a mixed grip, or hook grip. Relax the shoulders, which in effect lengthens your arms. Take a breath, and then lower your hips, looking forward with your head with your chest up. Drive through the floor, spreading your feet apart, with your weight on the back half of your feet. Extend through the hips and knees.'
    },
    'sumo_squat': {
        'display_name': 'Sumo Squat',
        'category': 'lower_body',
        'met_value': 5.0,
        'mode': 'rep',
        'angles': {
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
        },
        'primary_angle': 'left_knee',
        'down_threshold': 90,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Knees caving in', 'check': 'knee_alignment_x', 'severity': 'RED'},
            {'name': 'Not deep enough', 'check': 'primary_angle_gt_at_bottom:110', 'severity': 'YELLOW'},
        ],
        'description': 'Perform a squat with a wide stance and toes pointed outward to target the inner thighs.'
    },
    'superman': {
        'display_name': 'Superman',
        'category': 'upper_body',
        'met_value': 3.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
        },
        'primary_angle': 'back',
        'down_threshold': 170,
        'up_threshold': 150,
        'form_rules': [
            {'name': 'Insufficient lift', 'check': 'back_angle_gt:165', 'severity': 'YELLOW'},
        ],
        'description': 'Lie face down and raise your arms, chest, and legs off the floor to strengthen the lower back.'
    },
    't_bar_row': {
        'display_name': 'T-Bar Row',
        'category': 'upper_body',
        'met_value': 5.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 80,
        'form_rules': [
            {'name': 'Incomplete pull', 'check': 'primary_angle_gt_at_top:95', 'severity': 'YELLOW'},
        ],
        'description': 'Load up the T-bar Row Machine with the desired weight and adjust the leg height so that your upper chest is at the top of the pad. Tip: In some machines all you can do is stand on the appropriate step that allows you to be at a height that has the upper chest at the top of the pad. Lay face down on the pad and grab the handles. You can either use a palms down, palms up, or palms in position depending on what part of your back you want to emphasize.'
    },
    'towel_row': {
        'display_name': 'Towel Row',
        'category': 'upper_body',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 145,
        'up_threshold': 80,
        'form_rules': [
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:130', 'severity': 'YELLOW'},
        ],
        'description': 'Pull against a towel or strap wrapped around an anchor to perform a rowing motion.'
    },
    'tricep_dip': {
        'display_name': 'Tricep Dip',
        'category': 'upper_body',
        'met_value': 5.0,
        'mode': 'rep',
        'angles': {
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 90,
        'up_threshold': 155,
        'form_rules': [
            {'name': 'Not deep enough', 'check': 'primary_angle_gt_at_bottom:105', 'severity': 'YELLOW'},
        ],
        'description': 'Lower and raise your body using parallel bars or a bench to target the triceps.'
    },
    'wall_pushup': {
        'display_name': 'Wall Pushup',
        'category': 'upper_body',
        'met_value': 3.0,
        'mode': 'rep',
        'angles': {
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 90,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Incomplete lock out', 'check': 'primary_angle_lt_at_bottom:145', 'severity': 'YELLOW'},
        ],
        'description': 'Perform a pushup against a wall to reduce resistance and focus on shoulder/chest activation.'
    },
    'wall_sit': {
        'display_name': 'Wall Sit',
        'category': 'lower_body',
        'met_value': 3.0,
        'mode': 'hold',
        'angles': {
            'knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
        },
        'primary_angle': 'left_knee',
        'down_threshold': 80,
        'up_threshold': 110,
        'form_rules': [
            {'name': 'Knees caving in', 'check': 'knee_alignment_x', 'severity': 'RED'},
            {'name': 'Hip too high', 'check': 'primary_angle_gt:115', 'severity': 'RED'},
        ],
        'description': 'Lean against a wall with knees bent at 90 degrees and hold the position to build quadriceps endurance.'
    },
    'wide_grip_pull_up': {
        'display_name': 'Wide-Grip Pull-Up',
        'category': 'upper_body',
        'met_value': 8.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 145,
        'up_threshold': 75,
        'form_rules': [
            {'name': 'Incomplete range', 'check': 'primary_angle_gt_at_top:95', 'severity': 'YELLOW'},
        ],
        'description': 'Hang from a bar with a wide overhand grip and pull yourself up to engage the outer lats.'
    },
    'zottman_curl': {
        'display_name': 'Zottman Curl',
        'category': 'upper_body',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 45,
        'form_rules': [
            {'name': 'Incomplete rotation', 'check': 'primary_angle_lt_at_bottom:130', 'severity': 'YELLOW'},
        ],
        'description': 'Stand up with your torso upright and a dumbbell in each hand being held at arms length. The elbows should be close to the torso. Make sure the palms of the hands are facing each other. This will be your starting position.'
    },

    # ================================================================
    # CHEST EXERCISES (10 new)  — Source: yuhonas/free-exercise-db (MIT)
    # Angle configs hand-derived anatomically.
    # ================================================================

    'around_the_world': {
        'display_name': 'Around The Worlds',
        'category': 'upper_body',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 30,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Elbows bent too much', 'check': 'left_elbow_angle_lt:130', 'severity': 'YELLOW'},
            {'name': 'Incomplete arc', 'check': 'primary_angle_lt_at_bottom:140', 'severity': 'YELLOW'},
        ],
        'description': 'Lay down on a flat bench holding a dumbbell in each hand with the palms of the hands facing towards the ceiling. Extend your arms perpendicular to your torso and arc them in a wide circular motion overhead then back, keeping a slight bend in the elbows throughout.'
    },

    'alternating_floor_press': {
        'display_name': 'Alternating Floor Press',
        'category': 'upper_body',
        'met_value': 5.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 90,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Not deep enough', 'check': 'primary_angle_gt_at_bottom:110', 'severity': 'YELLOW'},
            {'name': 'Excessive arch', 'check': 'back_angle_lt:140', 'severity': 'YELLOW'},
        ],
        'description': 'Lie on the floor with two kettlebells or dumbbells next to your shoulders. Press one arm at a time to full extension, lowering it as you press the other, maintaining control and keeping your back flat on the floor.'
    },

    'bodyweight_fly': {
        'display_name': 'Bodyweight Flyes',
        'category': 'upper_body',
        'met_value': 6.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 95,
        'up_threshold': 155,
        'form_rules': [
            {'name': 'Sagging hips', 'check': 'back_angle_lt:140', 'severity': 'RED'},
            {'name': 'Arms not wide enough', 'check': 'primary_angle_lt_at_bottom:140', 'severity': 'YELLOW'},
        ],
        'description': 'Position two equally loaded bars on the ground next to each other and get into a push-up position with one hand on each bar. Slowly slide or roll the bars apart, lowering your chest toward the floor in a fly motion, then bring them back together.'
    },

    'butterfly_machine': {
        'display_name': 'Butterfly Machine (Pec Deck)',
        'category': 'upper_body',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 80,
        'up_threshold': 150,
        'form_rules': [
            {'name': 'Incomplete contraction', 'check': 'primary_angle_gt_at_top:130', 'severity': 'YELLOW'},
            {'name': 'Overextending', 'check': 'left_shoulder_angle_lt:70', 'severity': 'YELLOW'},
        ],
        'description': 'Sit on the pec deck machine with your back flat on the pad. Grasp the handles at your sides and squeeze your arms together in front of your chest, then slowly return to the start position maintaining control throughout.'
    },

    'cable_chest_press': {
        'display_name': 'Cable Chest Press',
        'category': 'upper_body',
        'met_value': 5.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 85,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:145', 'severity': 'YELLOW'},
            {'name': 'Excessive lean', 'check': 'back_angle_lt:155', 'severity': 'YELLOW'},
        ],
        'description': 'Adjust the weight to an appropriate amount and be seated or stand at a cable machine, grasping the handles at chest height. Press the handles forward to full elbow extension, squeezing the chest at the peak, then return with control.'
    },

    'decline_dumbbell_fly': {
        'display_name': 'Decline Dumbbell Fly',
        'category': 'upper_body',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 90,
        'up_threshold': 150,
        'form_rules': [
            {'name': 'Elbows bent too much', 'check': 'left_elbow_angle_lt:110', 'severity': 'YELLOW'},
            {'name': 'Incomplete adduction', 'check': 'primary_angle_gt_at_top:130', 'severity': 'YELLOW'},
        ],
        'description': 'Secure your legs at the end of a decline bench and hold a dumbbell in each hand. Lower the dumbbells out to the sides in a wide arc until you feel a stretch across your chest, then squeeze the pecs to bring the weights back together above your chest.'
    },

    'chest_squeeze_press': {
        'display_name': 'Chest Squeeze Press',
        'category': 'upper_body',
        'met_value': 4.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 80,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Incomplete lockout', 'check': 'primary_angle_lt_at_bottom:145', 'severity': 'YELLOW'},
            {'name': 'Elbows drifting wide', 'check': 'right_elbow_angle_lt:110', 'severity': 'YELLOW'},
        ],
        'description': 'Lie on a flat bench holding two dumbbells pressed firmly together at chest level. Keeping constant inward pressure between the dumbbells, press them upward to arm extension and lower back with control — the squeeze activates the inner chest throughout the rep.'
    },

    'dumbbell_pullover': {
        'display_name': 'Dumbbell Pullover',
        'category': 'upper_body',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 30,
        'up_threshold': 100,
        'form_rules': [
            {'name': 'Elbows flaring', 'check': 'left_elbow_angle_lt:130', 'severity': 'YELLOW'},
            {'name': 'Insufficient stretch', 'check': 'primary_angle_gt_at_bottom:55', 'severity': 'YELLOW'},
        ],
        'description': 'Place a dumbbell standing up on a flat bench. Lie perpendicular to the bench with only your upper back supported, hips below bench height. Hold the dumbbell overhead with both hands, lower it in an arc behind your head until you feel a chest and lat stretch, then pull it back overhead.'
    },

    'single_arm_cable_fly': {
        'display_name': 'Single-Arm Cable Fly',
        'category': 'upper_body',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 80,
        'up_threshold': 145,
        'form_rules': [
            {'name': 'Elbow bend too much', 'check': 'left_elbow_angle_lt:120', 'severity': 'YELLOW'},
            {'name': 'Torso rotating', 'check': 'back_angle_lt:155', 'severity': 'YELLOW'},
        ],
        'description': 'Stand sideways to a cable machine with a single handle at chest height. With a slight elbow bend, pull the cable across your body in a sweeping arc, squeezing the pec at the midline, then return under control. Keep your torso square and avoid rotating.'
    },

    'svend_press': {
        'display_name': 'Svend Press',
        'category': 'upper_body',
        'met_value': 3.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 85,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:145', 'severity': 'YELLOW'},
            {'name': 'Elbows too wide', 'check': 'right_elbow_angle_lt:130', 'severity': 'YELLOW'},
        ],
        'description': 'Stand holding two small weight plates pressed firmly together at chest height with both palms. Press the plates directly outward to arm extension while keeping constant squeezing pressure between them, then return to the chest. The isometric pressing action maximises inner-chest tension.'
    },

    # ================================================================
    # BACK EXERCISES (12 new)  — Source: yuhonas/free-exercise-db (MIT)
    # ================================================================

    'alternating_kettlebell_row': {
        'display_name': 'Alternating Kettlebell Row',
        'category': 'upper_body',
        'met_value': 5.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 75,
        'form_rules': [
            {'name': 'Rounded back', 'check': 'back_angle_lt:140', 'severity': 'RED'},
            {'name': 'Incomplete pull', 'check': 'primary_angle_gt_at_top:90', 'severity': 'YELLOW'},
        ],
        'description': 'Place two kettlebells in front of your feet. Bend your knees slightly and push your hips back with your back flat. Row one kettlebell up toward your hip, lower it, then row the other side, alternating in a controlled rhythm without rotating your torso.'
    },

    'renegade_row': {
        'display_name': 'Renegade Row',
        'category': 'upper_body',
        'met_value': 7.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 75,
        'form_rules': [
            {'name': 'Hips rotating', 'check': 'back_angle_lt:140', 'severity': 'RED'},
            {'name': 'Incomplete pull', 'check': 'primary_angle_gt_at_top:90', 'severity': 'YELLOW'},
        ],
        'description': 'Place two kettlebells on the floor shoulder-width apart and get into a pushup position gripping the handles. Row one kettlebell to your hip while the other arm supports your weight, then lower and repeat on the other side, keeping your hips square to the floor.'
    },

    'bent_arm_barbell_pullover': {
        'display_name': 'Bent-Arm Barbell Pullover',
        'category': 'upper_body',
        'met_value': 4.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 30,
        'up_threshold': 95,
        'form_rules': [
            {'name': 'Arms straightening', 'check': 'left_elbow_angle_lt:90', 'severity': 'YELLOW'},
            {'name': 'Insufficient stretch', 'check': 'primary_angle_gt_at_bottom:55', 'severity': 'YELLOW'},
        ],
        'description': 'Lie on a flat bench with a barbell using a shoulder-width grip. With elbows bent at approximately 90 degrees, lower the bar in an arc overhead toward the floor until you feel a stretch through the lats, then pull it back over your chest using your lats and chest.'
    },

    'dumbbell_incline_row': {
        'display_name': 'Dumbbell Incline Row',
        'category': 'upper_body',
        'met_value': 4.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 155,
        'up_threshold': 75,
        'form_rules': [
            {'name': 'Rounded upper back', 'check': 'back_angle_lt:140', 'severity': 'RED'},
            {'name': 'Incomplete contraction', 'check': 'primary_angle_gt_at_top:95', 'severity': 'YELLOW'},
        ],
        'description': 'Using a neutral grip, lean chest-down into an incline bench set to about 45 degrees. With a dumbbell in each hand hanging toward the floor, row them simultaneously toward your hips, squeezing the shoulder blades together at the top, then lower with control.'
    },

    'close_grip_lat_pulldown': {
        'display_name': 'Close-Grip Lat Pulldown',
        'category': 'upper_body',
        'met_value': 4.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 145,
        'up_threshold': 65,
        'form_rules': [
            {'name': 'Leaning too far back', 'check': 'back_angle_lt:130', 'severity': 'YELLOW'},
            {'name': 'Incomplete pull', 'check': 'primary_angle_gt_at_top:85', 'severity': 'YELLOW'},
        ],
        'description': 'Sit down on a pull-down machine with a close-grip V-bar or parallel handles attached to the top pulley. Pull the bar down to your upper chest by driving your elbows toward your hips, leaning slightly back, and squeezing the lats at the bottom position.'
    },

    'elevated_cable_row': {
        'display_name': 'Elevated Cable Row',
        'category': 'upper_body',
        'met_value': 4.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 80,
        'form_rules': [
            {'name': 'Hunching back', 'check': 'back_angle_lt:145', 'severity': 'RED'},
            {'name': 'Pulling too wide', 'check': 'primary_angle_gt_at_top:100', 'severity': 'YELLOW'},
        ],
        'description': 'Stand on a raised platform facing a low cable pulley, grasping two stirrup handles. With a hip-width stance and slight knee bend, row the handles toward your lower ribs, driving the elbows back and squeezing the shoulder blades together, then extend the arms fully.'
    },

    'bent_over_two_dumbbell_row': {
        'display_name': 'Bent Over Two-Dumbbell Row',
        'category': 'upper_body',
        'met_value': 5.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 75,
        'form_rules': [
            {'name': 'Rounded back', 'check': 'back_angle_lt:140', 'severity': 'RED'},
            {'name': 'Standing too upright', 'check': 'back_angle_gt:165', 'severity': 'YELLOW'},
            {'name': 'Incomplete pull', 'check': 'primary_angle_gt_at_top:95', 'severity': 'YELLOW'},
        ],
        'description': 'With a dumbbell in each hand and palms facing your torso, bend your knees slightly and hinge at the hips until your torso is nearly parallel to the floor. Keeping the back straight, row both dumbbells simultaneously toward your hips, then lower with control.'
    },

    'band_assisted_pull_up': {
        'display_name': 'Band Assisted Pull-Up',
        'category': 'upper_body',
        'met_value': 6.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 155,
        'up_threshold': 65,
        'form_rules': [
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:135', 'severity': 'YELLOW'},
            {'name': 'Kipping', 'check': 'back_angle_lt:155', 'severity': 'YELLOW'},
        ],
        'description': 'Choke a resistance band around the center of a pull-up bar and place your knees or feet in the loop. Grip the bar with an overhand grip wider than shoulder width and pull yourself up until your chin clears the bar, then lower under control to full arm extension.'
    },

    'seated_row_wide_grip': {
        'display_name': 'Seated Row — Wide Grip',
        'category': 'upper_body',
        'met_value': 4.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 155,
        'up_threshold': 80,
        'form_rules': [
            {'name': 'Leaning back too much', 'check': 'back_angle_lt:130', 'severity': 'YELLOW'},
            {'name': 'Hunching forward', 'check': 'back_angle_gt:185', 'severity': 'RED'},
            {'name': 'Incomplete pull', 'check': 'primary_angle_gt_at_top:100', 'severity': 'YELLOW'},
        ],
        'description': 'Sit at a cable row station with your feet on the platform and knees slightly bent. Grip a wide bar with an overhand grip outside shoulder width. Keeping an upright torso, row the bar to your upper abdomen by driving the elbows back and squeezing the rear delts and traps.'
    },

    'straight_arm_lat_pulldown': {
        'display_name': 'Straight-Arm Lat Pulldown',
        'category': 'upper_body',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 35,
        'up_threshold': 105,
        'form_rules': [
            {'name': 'Bending elbows', 'check': 'left_elbow_angle_lt:135', 'severity': 'YELLOW'},
            {'name': 'Insufficient pulldown', 'check': 'primary_angle_gt_at_bottom:55', 'severity': 'YELLOW'},
        ],
        'description': 'Stand facing a high cable pulley and grip a straight bar with arms fully extended. Keeping a slight forward lean and the elbows almost straight, pull the bar down in a wide arc to your thighs by engaging the lats, then raise back to the start with control.'
    },

    'single_arm_lat_pulldown': {
        'display_name': 'Single-Arm Lat Pulldown',
        'category': 'upper_body',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 140,
        'up_threshold': 65,
        'form_rules': [
            {'name': 'Leaning too far', 'check': 'back_angle_lt:130', 'severity': 'YELLOW'},
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:120', 'severity': 'YELLOW'},
        ],
        'description': 'Attach a single handle to a high cable pulley. Sit at a lat pulldown station and grasp the handle with one hand. Pull the handle down toward your shoulder by driving the elbow toward your hip, keeping the torso upright, then control the return to a full arm extension.'
    },

    'meadows_row': {
        'display_name': "Meadows Row",
        'category': 'upper_body',
        'met_value': 5.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 155,
        'up_threshold': 70,
        'form_rules': [
            {'name': 'Rounded back', 'check': 'back_angle_lt:140', 'severity': 'RED'},
            {'name': 'Incomplete contraction', 'check': 'primary_angle_gt_at_top:90', 'severity': 'YELLOW'},
        ],
        'description': 'Stand perpendicular to a landmine bar (or barbell anchored in a corner) with your working-side foot forward. Hinge at the hip until your torso is roughly parallel to the floor and grip the end of the bar with a pronated grip. Row the bar toward your hip by driving the elbow up and back, squeezing the lat hard at the top.'
    },

    # ================================================================
    # DEADLIFT VARIATIONS (3 new)  — Source: yuhonas/free-exercise-db (MIT)
    # All use lower_body category (consistent with existing conventional_deadlift,
    # romanian_deadlift, sumo_deadlift).
    # Rounded-back detection via back_angle_lt RED rule on all three.
    # ================================================================

    'trap_bar_deadlift': {
        'display_name': 'Trap Bar Deadlift',
        'category': 'lower_body',
        'met_value': 6.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'hip',
        'down_threshold': 100,
        'up_threshold': 170,
        'form_rules': [
            {'name': 'Rounded back', 'check': 'back_angle_lt:140', 'severity': 'RED'},
            {'name': 'Knees caving', 'check': 'knee_alignment_x', 'severity': 'RED'},
            {'name': 'Not deep enough at setup', 'check': 'primary_angle_gt_at_bottom:125', 'severity': 'YELLOW'},
        ],
        'description': 'Stand inside a loaded trap/hex bar with feet hip-width apart. Hinge at the hips and bend the knees to grip the handles with a neutral grip. Keeping your chest up and back flat, drive through the floor to stand fully upright, then hinge back down with control to return the bar.'
    },

    'deficit_deadlift': {
        'display_name': 'Deficit Deadlift',
        'category': 'lower_body',
        'met_value': 6.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'hip',
        'down_threshold': 95,
        'up_threshold': 170,
        'form_rules': [
            {'name': 'Rounded back', 'check': 'back_angle_lt:135', 'severity': 'RED'},
            {'name': 'Knees caving', 'check': 'knee_alignment_x', 'severity': 'RED'},
            {'name': 'Insufficient depth', 'check': 'primary_angle_gt_at_bottom:120', 'severity': 'YELLOW'},
        ],
        'description': 'Stand on a 1–3 inch platform or weight plates with a loaded barbell on the floor below. Approach and grip the bar in your conventional stance. The elevated position increases the range of motion, requiring deeper hip and knee flexion at the start — keep the back flat and drive hard through the legs to lockout.'
    },

    'stiff_leg_deadlift': {
        'display_name': 'Stiff-Leg Deadlift',
        'category': 'lower_body',
        'met_value': 5.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_knee': ['left_hip', 'left_knee', 'left_ankle'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
            'right_knee': ['right_hip', 'right_knee', 'right_ankle'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'hip',
        'down_threshold': 115,
        'up_threshold': 170,
        'form_rules': [
            {'name': 'Rounded back', 'check': 'back_angle_lt:140', 'severity': 'RED'},
            {'name': 'Excessive knee bend', 'check': 'left_knee_angle_lt:155', 'severity': 'YELLOW'},
            {'name': 'Insufficient hinge', 'check': 'primary_angle_gt_at_bottom:140', 'severity': 'YELLOW'},
        ],
        'description': 'Stand holding a barbell with an overhand shoulder-width grip. With your knees nearly locked and back flat, hinge at the hips to lower the bar along your shins until you feel a strong hamstring stretch, then drive the hips forward to return to the upright position. Keep the bar close to your body throughout.'
    },

    # ================================================================
    # TRICEPS EXERCISES (7 new)  — Source: yuhonas/free-exercise-db (MIT)
    # category: "triceps" as specified in prompt.
    # Angle configs hand-derived anatomically.
    # Primary movement: elbow extension — down_threshold > up_threshold (Case B)
    # ================================================================

    'cable_rope_overhead_tricep_extension': {
        'display_name': 'Cable Rope Overhead Tricep Extension',
        'category': 'triceps',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 80,
        'up_threshold': 155,
        'form_rules': [
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:140', 'severity': 'YELLOW'},
            {'name': 'Elbows flaring', 'check': 'back_angle_lt:150', 'severity': 'YELLOW'},
        ],
        'description': 'Attach a rope to the bottom pulley of a cable machine. Face away from the machine and hold the rope overhead with both hands. Keeping your upper arms close to your head, extend your elbows to full lockout, then slowly lower the rope behind your head.'
    },

    'cable_lying_tricep_extension': {
        'display_name': 'Cable Lying Tricep Extension',
        'category': 'triceps',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 80,
        'up_threshold': 155,
        'form_rules': [
            {'name': 'Elbows drifting back', 'check': 'left_shoulder_angle_lt:50', 'severity': 'YELLOW'},
            {'name': 'Incomplete lockout', 'check': 'primary_angle_lt_at_bottom:140', 'severity': 'YELLOW'},
        ],
        'description': 'Lie on a flat bench and grasp the straight bar attachment of a low pulley cable with a narrow overhand grip. With arms extended overhead perpendicular to the floor, bend only at the elbows to lower the bar toward your forehead, then extend back to the start.'
    },

    'cable_one_arm_tricep_extension': {
        'display_name': 'Cable One-Arm Tricep Extension',
        'category': 'triceps',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 85,
        'up_threshold': 155,
        'form_rules': [
            {'name': 'Elbow drifting forward', 'check': 'left_shoulder_angle_lt:45', 'severity': 'YELLOW'},
            {'name': 'Incomplete lockout', 'check': 'primary_angle_lt_at_bottom:140', 'severity': 'YELLOW'},
        ],
        'description': 'Grasp a single handle attached to a high cable pulley with an underhand grip. Keeping your upper arm stationary beside your head, extend the forearm downward to full lockout, then slowly return the handle overhead behind your head.'
    },

    'close_grip_dumbbell_press': {
        'display_name': 'Close-Grip Dumbbell Press',
        'category': 'triceps',
        'met_value': 5.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 85,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Not deep enough', 'check': 'primary_angle_gt_at_bottom:105', 'severity': 'YELLOW'},
            {'name': 'Elbows flaring wide', 'check': 'right_elbow_angle_lt:100', 'severity': 'YELLOW'},
        ],
        'description': 'Place a dumbbell standing up on a flat bench. Lie perpendicular to the bench so your shoulders are supported. Hold the dumbbell with both hands directly above your chest, thumbs and fingers wrapped around the handle. Lower the dumbbell toward your chest keeping elbows tucked, then press to full extension.'
    },

    'decline_dumbbell_tricep_extension': {
        'display_name': 'Decline Dumbbell Tricep Extension',
        'category': 'triceps',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 80,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Elbows drifting out', 'check': 'left_shoulder_angle_lt:40', 'severity': 'YELLOW'},
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:145', 'severity': 'YELLOW'},
        ],
        'description': 'Secure your legs at the end of a decline bench and lie down with a dumbbell in each hand. Raise your arms overhead so they are perpendicular to the floor, then bend only at the elbows to lower the dumbbells toward your forehead and press back up to full extension.'
    },

    'body_tricep_press': {
        'display_name': 'Body Tricep Press',
        'category': 'triceps',
        'met_value': 6.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 90,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Sagging hips', 'check': 'back_angle_lt:140', 'severity': 'RED'},
            {'name': 'Incomplete lockout', 'check': 'primary_angle_lt_at_bottom:145', 'severity': 'YELLOW'},
        ],
        'description': 'Position a barbell or bar in a rack at chest height. Grip the bar with a narrow overhand grip and lean your body at an angle, supported by your arms. Lower your head under the bar by bending the elbows, then press back to the start by fully extending the triceps.'
    },

    'close_grip_pushup_on_dumbbell': {
        'display_name': 'Close-Grip Push-Up on Dumbbell',
        'category': 'triceps',
        'met_value': 7.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 90,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Sagging hips', 'check': 'back_angle_lt:140', 'severity': 'RED'},
            {'name': 'Not deep enough', 'check': 'primary_angle_gt_at_bottom:110', 'severity': 'YELLOW'},
        ],
        'description': 'Lie on the floor and place both hands on a single upright dumbbell, supporting your weight on your toes. Keep your torso rigid and elbows tucked close to your sides as you lower your chest toward the dumbbell, then press back to full arm extension.'
    },

    # ================================================================
    # BICEPS EXERCISES (9 new)  — Source: yuhonas/free-exercise-db (MIT)
    # category: "biceps" as specified in prompt.
    # Primary movement: elbow flexion — down_threshold > up_threshold (Case B)
    # ================================================================

    'alternate_hammer_curl': {
        'display_name': 'Alternate Hammer Curl',
        'category': 'biceps',
        'met_value': 3.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 155,
        'up_threshold': 45,
        'form_rules': [
            {'name': 'Swinging back', 'check': 'back_angle_lt:160', 'severity': 'RED'},
            {'name': 'Incomplete curl', 'check': 'primary_angle_gt_at_top:65', 'severity': 'YELLOW'},
        ],
        'description': 'Stand upright with a dumbbell in each hand, palms facing your torso. Keeping the upper arm stationary, curl one dumbbell toward the shoulder with a neutral (hammer) grip, lower it, then curl the other side, alternating reps without swinging the back.'
    },

    'cable_hammer_curl': {
        'display_name': 'Cable Hammer Curl (Rope)',
        'category': 'biceps',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 155,
        'up_threshold': 50,
        'form_rules': [
            {'name': 'Swinging torso', 'check': 'back_angle_lt:158', 'severity': 'RED'},
            {'name': 'Incomplete contraction', 'check': 'primary_angle_gt_at_top:70', 'severity': 'YELLOW'},
        ],
        'description': 'Attach a rope to a low pulley and stand facing the machine about 12 inches away. With palms facing each other and elbows close to the torso, curl the rope to your shoulders squeezing the brachialis, then lower under control to full extension.'
    },

    'cable_preacher_curl': {
        'display_name': 'Cable Preacher Curl',
        'category': 'biceps',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 45,
        'form_rules': [
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:130', 'severity': 'YELLOW'},
            {'name': 'Lifting shoulder off pad', 'check': 'left_shoulder_angle_gt:85', 'severity': 'YELLOW'},
        ],
        'description': 'Place a preacher bench about two feet in front of a low pulley. Drape your upper arm over the angled pad and curl the cable handle from full extension to full flexion, keeping the arm pinned against the pad throughout to eliminate momentum.'
    },

    'ez_bar_curl': {
        'display_name': 'EZ-Bar Curl',
        'category': 'biceps',
        'met_value': 4.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 155,
        'up_threshold': 40,
        'form_rules': [
            {'name': 'Swinging back', 'check': 'back_angle_lt:160', 'severity': 'RED'},
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:135', 'severity': 'YELLOW'},
        ],
        'description': 'Stand upright holding an EZ curl bar at the wide outer handle with palms facing forward. Keeping the upper arms stationary and close to the torso, curl the bar upward by flexing the biceps, then lower with control to full elbow extension.'
    },

    'cross_body_hammer_curl': {
        'display_name': 'Cross Body Hammer Curl',
        'category': 'biceps',
        'met_value': 3.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 155,
        'up_threshold': 45,
        'form_rules': [
            {'name': 'Swinging back', 'check': 'back_angle_lt:158', 'severity': 'RED'},
            {'name': 'Shoulder swinging', 'check': 'left_shoulder_angle_gt:95', 'severity': 'YELLOW'},
        ],
        'description': 'Stand with a dumbbell in each hand and palms facing inward. Curl one dumbbell across your body toward the opposite shoulder, keeping the upper arm still, then lower and alternate sides. The cross-body path increases brachialis activation.'
    },

    'drag_curl': {
        'display_name': 'Drag Curl',
        'category': 'biceps',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 155,
        'up_threshold': 45,
        'form_rules': [
            {'name': 'Bar drifting forward', 'check': 'left_shoulder_angle_gt:80', 'severity': 'YELLOW'},
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:135', 'severity': 'YELLOW'},
        ],
        'description': 'Grab a barbell with a supinated grip and pull your elbows back behind your body as you curl — the bar drags up along your torso rather than arcing forward. This removes front-delt involvement and maximises peak biceps contraction.'
    },

    'high_cable_curl': {
        'display_name': 'High Cable Curl',
        'category': 'biceps',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 155,
        'up_threshold': 45,
        'form_rules': [
            {'name': 'Elbows dropping', 'check': 'left_shoulder_angle_lt:80', 'severity': 'YELLOW'},
            {'name': 'Incomplete contraction', 'check': 'primary_angle_gt_at_top:65', 'severity': 'YELLOW'},
        ],
        'description': 'Stand between two high pulleys and grab a handle in each hand with palms up. Position your upper arms parallel to the floor, then curl both handles toward your ears by contracting the biceps — only the forearms should move. Hold the peak contraction briefly.'
    },

    'lying_cable_curl': {
        'display_name': 'Lying Cable Curl',
        'category': 'biceps',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 155,
        'up_threshold': 40,
        'form_rules': [
            {'name': 'Shoulder rising', 'check': 'left_shoulder_angle_gt:90', 'severity': 'YELLOW'},
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:130', 'severity': 'YELLOW'},
        ],
        'description': 'Grab a straight or EZ bar attached to a low pulley and lie face-up on the floor or a bench with arms extended toward the pulley. Curl the bar toward your face by contracting the biceps while keeping your upper arms flat on the surface, then lower with control.'
    },

    'dumbbell_alternate_bicep_curl': {
        'display_name': 'Dumbbell Alternate Bicep Curl',
        'category': 'biceps',
        'met_value': 3.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 155,
        'up_threshold': 40,
        'form_rules': [
            {'name': 'Swinging back', 'check': 'back_angle_lt:160', 'severity': 'RED'},
            {'name': 'Incomplete curl', 'check': 'primary_angle_gt_at_top:60', 'severity': 'YELLOW'},
            {'name': 'Incomplete extension', 'check': 'primary_angle_lt_at_bottom:135', 'severity': 'YELLOW'},
        ],
        'description': 'Stand upright with a dumbbell in each hand at arms length, elbows close to the torso. Rotate the palm of each hand to face forward as you curl one dumbbell up to shoulder level, then lower it while raising the other — alternating sides each rep.'
    },

    # ================================================================
    # SHOULDER EXERCISES (6 new)  — Source: yuhonas/free-exercise-db (MIT)
    # category: "shoulders" as specified in prompt.
    # Angle configs hand-derived anatomically.
    # ================================================================

    'barbell_shoulder_press': {
        'display_name': 'Barbell Shoulder Press',
        'category': 'shoulders',
        'met_value': 6.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 80,
        'up_threshold': 165,
        'form_rules': [
            {'name': 'Incomplete lockout', 'check': 'primary_angle_lt_at_bottom:150', 'severity': 'YELLOW'},
            {'name': 'Excessive back arch', 'check': 'back_angle_lt:145', 'severity': 'RED'},
        ],
        'description': 'Sit on a bench with back support in a squat rack and position a barbell just above your head. Grab the barbell with a pronated grip slightly wider than shoulder width and press it overhead to full elbow extension, then lower it back to just above the upper chest.'
    },

    'alternating_deltoid_raise': {
        'display_name': 'Alternating Deltoid Raise',
        'category': 'shoulders',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 25,
        'up_threshold': 90,
        'form_rules': [
            {'name': 'Swinging torso', 'check': 'back_angle_lt:160', 'severity': 'RED'},
            {'name': 'Raise too high', 'check': 'primary_angle_gt:105', 'severity': 'YELLOW'},
            {'name': 'Bending elbows', 'check': 'left_elbow_angle_lt:145', 'severity': 'YELLOW'},
        ],
        'description': 'Stand holding a pair of dumbbells at your sides. Alternating arms, raise one dumbbell out to the side to shoulder height and the other directly in front to shoulder height, then lower and switch — targeting both the lateral and front deltoids with each rep.'
    },

    'barbell_rear_delt_row': {
        'display_name': 'Barbell Rear Delt Row',
        'category': 'shoulders',
        'met_value': 4.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'hip': ['left_shoulder', 'left_hip', 'left_knee'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'right_elbow': ['right_shoulder', 'right_elbow', 'right_wrist'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 150,
        'up_threshold': 80,
        'form_rules': [
            {'name': 'Rounded back', 'check': 'back_angle_lt:140', 'severity': 'RED'},
            {'name': 'Incomplete contraction', 'check': 'primary_angle_gt_at_top:100', 'severity': 'YELLOW'},
        ],
        'description': 'Stand holding a barbell with a wide overhand grip, elbows pointing outward. Hinge forward at the hips until your torso is nearly parallel to the floor, then row the bar up toward your upper chest by driving the elbows back and out — squeezing the rear delts at the top.'
    },

    'barbell_shrug': {
        'display_name': 'Barbell Shrug',
        'category': 'shoulders',
        'met_value': 4.0,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 20,
        'up_threshold': 50,
        'form_rules': [
            {'name': 'Rolling shoulders', 'check': 'back_angle_lt:158', 'severity': 'YELLOW'},
            {'name': 'Bending elbows', 'check': 'left_elbow_angle_lt:155', 'severity': 'YELLOW'},
        ],
        'description': 'Stand upright holding a barbell in front of you with a pronated shoulder-width grip. Keeping the arms straight, elevate your shoulders as high as possible toward your ears, hold briefly to contract the traps, then lower under full control.'
    },

    'cable_rear_delt_fly': {
        'display_name': 'Cable Rear Delt Fly',
        'category': 'shoulders',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
            'right_shoulder': ['right_hip', 'right_shoulder', 'right_elbow'],
        },
        'primary_angle': 'left_shoulder',
        'down_threshold': 60,
        'up_threshold': 140,
        'form_rules': [
            {'name': 'Elbows bent too much', 'check': 'left_elbow_angle_lt:130', 'severity': 'YELLOW'},
            {'name': 'Incomplete abduction', 'check': 'primary_angle_gt_at_top:120', 'severity': 'YELLOW'},
        ],
        'description': 'Adjust two cable pulleys to above-head height and cross the handles. Stand between the towers and, with a slight elbow bend, pull each handle diagonally outward and downward in a wide arc to fully abduct the rear deltoids, then return with control.'
    },

    'cuban_press': {
        'display_name': 'Cuban Press',
        'category': 'shoulders',
        'met_value': 3.5,
        'mode': 'rep',
        'angles': {
            'back': ['left_shoulder', 'left_hip', 'left_ankle'],
            'left_elbow': ['left_shoulder', 'left_elbow', 'left_wrist'],
            'left_shoulder': ['left_hip', 'left_shoulder', 'left_elbow'],
        },
        'primary_angle': 'left_elbow',
        'down_threshold': 85,
        'up_threshold': 160,
        'form_rules': [
            {'name': 'Incomplete rotation', 'check': 'primary_angle_lt_at_bottom:140', 'severity': 'YELLOW'},
            {'name': 'Elbows dropping', 'check': 'left_shoulder_angle_lt:75', 'severity': 'YELLOW'},
        ],
        'description': 'Hold a dumbbell in each hand with a pronated grip and raise your upper arms to shoulder height, elbows bent 90 degrees. Rotate your forearms upward until they point to the ceiling (external rotation), then press the dumbbells overhead to full extension, reversing to return.'
    },
}


