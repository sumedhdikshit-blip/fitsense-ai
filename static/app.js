// FitSense AI Frontend Logic

let stream = null;
let socket = null;
let sendInterval = null;
let isSending = false;
let reconnectTimer = null;
let pingTimeout = null;

// Workout session & state variables
let currentExerciseKey = "";
let currentSetNumber = 1;
let lastRepsCounted = 0;
let lastAvgFormScore = 100;
let sessionSets = 0;
let sessionReps = 0;
let sessionAvgScore = 100;
let currentSessionId = null;

// Part 2 Additions
let isHoldMode = false;
let workoutStartTime = 0;
let activeProfile = null;
let selectedWeightDays = "90";
let activeCardioTab = "duration"; // "duration" | "direct"

// DOM Elements
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const canvasPlaceholder = document.getElementById('canvasPlaceholder');

const exerciseSelect = document.getElementById('exerciseSelect');
const startBtn = document.getElementById('startBtn');
const endSetBtn = document.getElementById('endSetBtn');
const endSessionBtn = document.getElementById('endSessionBtn');

const repLabelEl = document.getElementById('repLabel');
const repCountEl = document.getElementById('repCount');
const stageLabelEl = document.getElementById('stageLabel');
const formScorePercentEl = document.getElementById('formScorePercent');
const formScoreBarEl = document.getElementById('formScoreBar');
const feedbackContainer = document.getElementById('feedbackContainer');
const anglesContainer = document.getElementById('anglesContainer');
const streamStatusEl = document.getElementById('streamStatus');

// Log Set Modal Elements
const logSetModal = document.getElementById('logSetModal');
const modalExercise = document.getElementById('modalExercise');
const modalReps = document.getElementById('modalReps');
const modalRepsLabel = document.getElementById('modalRepsLabel');
const modalScore = document.getElementById('modalScore');
const weightInput = document.getElementById('weightInput');
const weightModeSelect = document.getElementById('weightModeSelect');
const setDurationInput = document.getElementById('setDurationInput');
const rpeInput = document.getElementById('rpeInput');
const rpeValue = document.getElementById('rpeValue');
const painCheckbox = document.getElementById('painCheckbox');
const painLocationGroup = document.getElementById('painLocationGroup');
const painLocationInput = document.getElementById('painLocationInput');
const saveSetBtn = document.getElementById('saveSetBtn');
const cancelSetBtn = document.getElementById('cancelSetBtn');

// Session Summary Modal Elements
const summaryModal = document.getElementById('summaryModal');
const sumSetsEl = document.getElementById('sumSets');
const sumRepsEl = document.getElementById('sumReps');
const sumRepsLabel = document.getElementById('sumRepsLabel');
const sumCaloriesEl = document.getElementById('sumCalories');
const sumScoreEl = document.getElementById('sumScore');
const sessionNotes = document.getElementById('sessionNotes');
const saveSessionBtn = document.getElementById('saveSessionBtn');

// Session Detail Modal Elements
const detailModal = document.getElementById('detailModal');
const closeDetailBtn = document.getElementById('closeDetailBtn');
const detailTitle = document.getElementById('detailTitle');
const detDate = document.getElementById('detDate');
const detDuration = document.getElementById('detDuration');
const detCalories = document.getElementById('detCalories');
const detForm = document.getElementById('detForm');
const detNotes = document.getElementById('detNotes');
const detailSetsBody = document.getElementById('detailSetsBody');

const historyBody = document.getElementById('historyBody');

// Part 2 UI Elements
const setupBanner = document.getElementById('setupBanner');
const bannerSetupBtn = document.getElementById('bannerSetupBtn');
const headerProfileBtn = document.getElementById('headerProfileBtn');
const avatarBadge = document.getElementById('avatarBadge');
const usernameEl = document.getElementById('username');

// Profile Modal Elements
const profileModal = document.getElementById('profileModal');
const closeProfileBtn = document.getElementById('closeProfileBtn');
const profileName = document.getElementById('profileName');
const profileAge = document.getElementById('profileAge');
const profileSex = document.getElementById('profileSex');
const profileWeight = document.getElementById('profileWeight');
const profileHeight = document.getElementById('profileHeight');
const profileGoal = document.getElementById('profileGoal');
const saveProfileBtn = document.getElementById('saveProfileBtn');

// Quick Weight Modal Elements
const quickWeightBtn = document.getElementById('quickWeightBtn');
const weightModal = document.getElementById('weightModal');
const closeWeightBtn = document.getElementById('closeWeightBtn');
const quickWeightInput = document.getElementById('quickWeightInput');
const quickWeightDate = document.getElementById('quickWeightDate');
const saveWeightBtn = document.getElementById('saveWeightBtn');
const currentWeightDisplay = document.getElementById('currentWeightDisplay');
const weightChangeDisplay = document.getElementById('weightChangeDisplay');

// Log Food Modal Elements
const logFoodBtn = document.getElementById('logFoodBtn');
const foodModal = document.getElementById('foodModal');
const closeFoodBtn = document.getElementById('closeFoodBtn');
const foodDate = document.getElementById('foodDate');
const foodCalories = document.getElementById('foodCalories');
const foodProtein = document.getElementById('foodProtein');
const foodCarbs = document.getElementById('foodCarbs');
const foodFat = document.getElementById('foodFat');
const saveFoodBtn = document.getElementById('saveFoodBtn');

// Log Cardio Modal Elements
const logCardioBtn = document.getElementById('logCardioBtn');
const cardioModal = document.getElementById('cardioModal');
const closeCardioBtn = document.getElementById('closeCardioBtn');
const tabDurationBtn = document.getElementById('tabDurationBtn');
const tabDirectBtn = document.getElementById('tabDirectBtn');
const cardioDate = document.getElementById('cardioDate');
const panelDuration = document.getElementById('panelDuration');
const panelDirect = document.getElementById('panelDirect');
const cardioPresetSelect = document.getElementById('cardioPresetSelect');
const cardioDuration = document.getElementById('cardioDuration');
const customMetGroup = document.getElementById('customMetGroup');
const cardioCustomMet = document.getElementById('cardioCustomMet');
const cardioEstimatedDisplay = document.getElementById('cardioEstimatedDisplay');
const overrideCalorieCheckbox = document.getElementById('overrideCalorieCheckbox');
const overrideCalorieGroup = document.getElementById('overrideCalorieGroup');
const cardioOverrideVal = document.getElementById('cardioOverrideVal');
const cardioActivityName = document.getElementById('cardioActivityName');
const cardioDirectCalories = document.getElementById('cardioDirectCalories');
const cardioDirectDuration = document.getElementById('cardioDirectDuration');
const saveCardioBtn = document.getElementById('saveCardioBtn');

// Calorie Board Display Elements
const netCaloriesDisplay = document.getElementById('netCaloriesDisplay');
const calsConsumedEl = document.getElementById('calsConsumed');
const calsBurnedEl = document.getElementById('calsBurned');
const calsBmrEl = document.getElementById('calsBmr');
const calsTefEl = document.getElementById('calsTef');
const macroProteinEl = document.getElementById('macroProtein');
const macroCarbsEl = document.getElementById('macroCarbs');
const macroFatEl = document.getElementById('macroFat');

// Initialization
document.addEventListener('DOMContentLoaded', async () => {
  setupEventListeners();
  await fetchProfile();
  await fetchExercises();
  await fetchRecentSessions();
  await refreshDashboard();
});

// Setup Events
function setupEventListeners() {
  startBtn.addEventListener('click', startWorkout);
  endSetBtn.addEventListener('click', endSet);
  endSessionBtn.addEventListener('click', endSession);
  
  // Pain checkbox visibility toggle
  painCheckbox.addEventListener('change', (e) => {
    painLocationGroup.style.display = e.target.checked ? 'flex' : 'none';
  });
  
  // RPE value update
  rpeInput.addEventListener('input', (e) => {
    rpeValue.textContent = e.target.value;
  });
  
  // Modal save/cancel
  saveSetBtn.addEventListener('click', saveSet);
  cancelSetBtn.addEventListener('click', discardSet);
  saveSessionBtn.addEventListener('click', saveSession);
  
  closeDetailBtn.addEventListener('click', () => {
    detailModal.classList.remove('active');
  });

  // Profile modal bindings
  const openProfile = () => {
    if (activeProfile) {
      profileName.value = activeProfile.name || "";
      profileAge.value = activeProfile.age || "";
      profileSex.value = activeProfile.sex || "unspecified";
      profileWeight.value = activeProfile.weight_kg || "";
      profileHeight.value = activeProfile.height_cm || "";
      profileGoal.value = activeProfile.fitness_goal || "";
    }
    profileModal.classList.add('active');
  };
  headerProfileBtn.addEventListener('click', openProfile);
  bannerSetupBtn.addEventListener('click', openProfile);
  closeProfileBtn.addEventListener('click', () => profileModal.classList.remove('active'));
  saveProfileBtn.addEventListener('click', saveProfile);

  // Quick weight bindings
  quickWeightBtn.addEventListener('click', () => {
    quickWeightInput.value = activeProfile ? activeProfile.weight_kg : 75.0;
    quickWeightDate.value = new Date().toISOString().split('T')[0];
    weightModal.classList.add('active');
  });
  closeWeightBtn.addEventListener('click', () => weightModal.classList.remove('active'));
  saveWeightBtn.addEventListener('click', saveWeight);

  // Food modal bindings
  logFoodBtn.addEventListener('click', () => {
    foodDate.value = new Date().toISOString().split('T')[0];
    foodCalories.value = "";
    foodProtein.value = 0;
    foodCarbs.value = 0;
    foodFat.value = 0;
    foodModal.classList.add('active');
  });
  closeFoodBtn.addEventListener('click', () => foodModal.classList.remove('active'));
  saveFoodBtn.addEventListener('click', saveFood);

  // Cardio modal bindings
  logCardioBtn.addEventListener('click', () => {
    cardioDate.value = new Date().toISOString().split('T')[0];
    cardioDuration.value = 30;
    cardioOverrideVal.value = "";
    overrideCalorieCheckbox.checked = false;
    overrideCalorieGroup.style.display = "none";
    cardioActivityName.value = "";
    cardioDirectCalories.value = "";
    cardioDirectDuration.value = "";
    customMetGroup.style.display = "none";
    updateCardioEstimate();
    cardioModal.classList.add('active');
  });
  closeCardioBtn.addEventListener('click', () => cardioModal.classList.remove('active'));
  saveCardioBtn.addEventListener('click', saveCardio);

  // Cardio tab triggers
  tabDurationBtn.addEventListener('click', () => {
    activeCardioTab = "duration";
    tabDurationBtn.classList.add('active');
    tabDirectBtn.classList.remove('active');
    panelDuration.style.display = "block";
    panelDirect.style.display = "none";
  });
  tabDirectBtn.addEventListener('click', () => {
    activeCardioTab = "direct";
    tabDirectBtn.classList.add('active');
    tabDurationBtn.classList.remove('active');
    panelDuration.style.display = "none";
    panelDirect.style.display = "block";
  });

  cardioPresetSelect.addEventListener('change', (e) => {
    customMetGroup.style.display = e.target.value === "Other" ? "flex" : "none";
    updateCardioEstimate();
  });
  cardioDuration.addEventListener('input', updateCardioEstimate);
  cardioCustomMet.addEventListener('input', updateCardioEstimate);
  overrideCalorieCheckbox.addEventListener('change', (e) => {
    overrideCalorieGroup.style.display = e.target.checked ? "flex" : "none";
  });

  // Exercise dropdown logic change for hold mode UI
  exerciseSelect.addEventListener('change', () => {
    const selectedOpt = exerciseSelect.options[exerciseSelect.selectedIndex];
    const mode = selectedOpt.getAttribute('data-mode');
    if (mode === "hold") {
      isHoldMode = true;
      repLabelEl.textContent = "HOLD TIME";
    } else {
      isHoldMode = false;
      repLabelEl.textContent = "REPS";
    }
  });

  // Chart range selector buttons
  document.querySelectorAll('.btn-range').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      document.querySelectorAll('.btn-range').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      selectedWeightDays = e.target.getAttribute('data-days');
      await fetchWeightHistoryAndDraw();
    });
  });
}

// Fetch dynamic user profile from backend
async function fetchProfile() {
  try {
    const response = await fetch('/profile');
    if (response.ok) {
      activeProfile = await response.json();
      
      // Update UI components
      usernameEl.textContent = activeProfile.name || "Athlete";
      avatarBadge.textContent = activeProfile.name ? activeProfile.name[0].toUpperCase() : "A";
      
      // Verify completeness
      const isComplete = activeProfile.weight_kg && activeProfile.height_cm && activeProfile.age && activeProfile.sex;
      setupBanner.style.display = isComplete ? "none" : "flex";
    }
  } catch (error) {
    console.error('Error fetching profile:', error);
  }
}

// Save User Profile settings
async function saveProfile() {
  const payload = {
    name: profileName.value || "Athlete",
    age: parseInt(profileAge.value) || 0,
    weight_kg: parseFloat(profileWeight.value) || 0.0,
    height_cm: parseFloat(profileHeight.value) || 0.0,
    sex: profileSex.value,
    fitness_goal: profileGoal.value || ""
  };

  try {
    const response = await fetch('/profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (response.ok) {
      profileModal.classList.remove('active');
      await fetchProfile();
      await refreshDashboard();
    } else {
      const err = await response.json();
      alert(`Error: ${err.detail || 'Validation failed. Age 1-120, Weight 10-500, Height 50-300.'}`);
    }
  } catch (error) {
    console.error('Error updating profile:', error);
  }
}

// Fetch exercises from config endpoint (50 exercises)
async function fetchExercises() {
  try {
    const response = await fetch('/exercises');
    const exercises = await response.json();
    
    exerciseSelect.innerHTML = '';
    
    const categories = {
      lower_body: 'Lower Body',
      upper_body: 'Upper Body',
      core: 'Core',
      cardio: 'Cardio & Full Body',
      flexibility: 'Flexibility & Mobility'
    };
    
    Object.keys(categories).forEach(catKey => {
      const catEx = exercises.filter(ex => ex.category === catKey);
      if (catEx.length > 0) {
        const group = document.createElement('optgroup');
        group.label = categories[catKey];
        catEx.forEach(ex => {
          const opt = document.createElement('option');
          opt.value = ex.key;
          opt.textContent = ex.display_name;
          opt.setAttribute('data-mode', ex.mode);
          group.appendChild(opt);
        });
        exerciseSelect.appendChild(group);
      }
    });
    
    // Set initial mode state
    if (exerciseSelect.options.length > 0) {
      const initialMode = exerciseSelect.options[0].getAttribute('data-mode');
      isHoldMode = (initialMode === "hold");
      repLabelEl.textContent = isHoldMode ? "HOLD TIME" : "REPS";
    }
    
    startBtn.disabled = false;
  } catch (error) {
    console.error('Error fetching exercises:', error);
  }
}

// Fetch session history
async function fetchRecentSessions() {
  try {
    const response = await fetch('/sessions/recent');
    const sessions = await response.json();
    
    if (sessions.length === 0) {
      historyBody.innerHTML = `
        <tr>
          <td colspan="7" style="text-align: center; color: #aaaaaa;">No workout history found. Log a session to get started.</td>
        </tr>
      `;
      return;
    }
    
    historyBody.innerHTML = '';
    sessions.forEach(sess => {
      const dateFormatted = new Date(sess.date).toLocaleDateString(undefined, {
        year: 'numeric', month: 'short', day: 'numeric'
      });
      
      const repsOrTime = sess.exercises_done && (sess.exercises_done.includes("Plank") || sess.exercises_done.includes("Hold") || sess.exercises_done.includes("Sit"))
        ? `${Math.round(sess.total_reps)}s` 
        : sess.total_reps;
        
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${dateFormatted}</td>
        <td>${sess.exercises_done || 'None'}</td>
        <td>${sess.total_sets}</td>
        <td>${repsOrTime}</td>
        <td>${sess.total_calories_burned ? sess.total_calories_burned.toFixed(1) + ' kcal' : '0 kcal'}</td>
        <td>
          <span class="${getScoreColorClass(sess.avg_form_score)}">
            ${Math.round(sess.avg_form_score)}%
          </span>
        </td>
        <td><span class="view-link" onclick="viewSessionDetails(${sess.session_id})">View Detail</span></td>
      `;
      historyBody.appendChild(tr);
    });
  } catch (error) {
    console.error('Error fetching history:', error);
  }
}

// View Session Detail
async function viewSessionDetails(sessionId) {
  try {
    const response = await fetch(`/sessions/${sessionId}`);
    const detail = await response.json();
    if (!detail) return;
    
    const dateFormatted = new Date(detail.date).toLocaleDateString(undefined, {
      year: 'numeric', month: 'short', day: 'numeric'
    });
    
    detailTitle.textContent = `Workout Session Details #${detail.session_id}`;
    detDate.textContent = dateFormatted;
    detDuration.textContent = detail.total_duration_mins ? detail.total_duration_mins.toFixed(1) : '0';
    detCalories.textContent = detail.total_calories_burned ? detail.total_calories_burned.toFixed(1) : '0';
    detForm.textContent = Math.round(detail.avg_form_score);
    detNotes.textContent = detail.notes || 'No notes added.';
    
    detailSetsBody.innerHTML = '';
    if (detail.exercises) {
      detail.exercises.forEach(ex => {
        const isExHold = (ex.exercise_key.includes("plank") || ex.exercise_key.includes("sit") || ex.exercise_key.includes("hold"));
        if (ex.sets) {
          ex.sets.forEach(set => {
            const durSuffix = (set.duration_seconds && set.duration_seconds > 0) ? ` (${set.duration_seconds.toFixed(1)}s)` : '';
            const setVol = (isExHold ? `${set.reps_counted}s` : set.reps_counted) + durSuffix;
            const weightModeLabel = set.weight_mode === 'per_side' ? ' (per side)' : ' (total)';
            const tr = document.createElement('tr');
            tr.innerHTML = `
              <td>Set ${set.set_number}</td>
              <td><strong>${ex.exercise_name}</strong></td>
              <td>${setVol}</td>
              <td>${set.weight_kg} kg${weightModeLabel}</td>
              <td>${set.rpe}</td>
              <td><span class="${getScoreColorClass(set.avg_form_score)}">${Math.round(set.avg_form_score)}%</span></td>
              <td>${set.pain_flag ? '<span class="score-red">YES (' + (set.pain_location || 'N/A') + ')</span>' : 'No'}</td>
            `;
            detailSetsBody.appendChild(tr);
          });
        }
      });
    }
    
    if (detailSetsBody.innerHTML === '') {
      detailSetsBody.innerHTML = '<tr><td colspan="7" style="text-align: center;">No sets found for this session.</td></tr>';
    }
    
    detailModal.classList.add('active');
  } catch (error) {
    console.error('Error fetching session details:', error);
  }
}

// Refresh Daily Dashboard Statistics
async function refreshDashboard() {
  try {
    const response = await fetch('/dashboard/today');
    if (response.ok) {
      const data = await response.json();
      
      // Update BMR, TEF, Net Calorie labels
      const nutrition = data.nutrition;
      
      const netVal = Math.round(nutrition.net_calories);
      netCaloriesDisplay.textContent = `${netVal > 0 ? '+' : ''}${netVal} kcal`;
      
      // Color-coding net calories
      if (netVal < 0) {
        netCaloriesDisplay.className = "net-cal-val deficit";
      } else if (netVal > 0) {
        netCaloriesDisplay.className = "net-cal-val surplus";
      } else {
        netCaloriesDisplay.className = "net-cal-val";
      }
      
      calsConsumedEl.textContent = `${Math.round(nutrition.calories_consumed)} kcal`;
      calsBurnedEl.textContent = `${Math.round(nutrition.calories_burned_exercise)} kcal`;
      calsBmrEl.textContent = `${Math.round(nutrition.calories_burned_bmr)} kcal`;
      calsTefEl.textContent = `${Math.round(nutrition.tef_calories)} kcal`;
      
      macroProteinEl.textContent = `${Math.round(nutrition.protein_g)}g`;
      macroCarbsEl.textContent = `${Math.round(nutrition.carbs_g)}g`;
      macroFatEl.textContent = `${Math.round(nutrition.fat_g)}g`;
      
      currentWeightDisplay.textContent = `${data.current_weight.toFixed(1)} kg`;
      
      // Redraw Weight history line chart
      await fetchWeightHistoryAndDraw();
    }
  } catch (error) {
    console.error('Error refreshing dashboard:', error);
  }
}

// Fetch weight history and plot on Canvas
async function fetchWeightHistoryAndDraw() {
  try {
    const response = await fetch(`/weight/history?days=${selectedWeightDays}`);
    if (response.ok) {
      const history = await response.json();
      drawWeightChart(history);
    }
  } catch (error) {
    console.error('Error loading weight history:', error);
  }
}

// Draw HTML5 Canvas Weight Chart
function drawWeightChart(data) {
  const canvas = document.getElementById('weightChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  
  if (!data || data.length === 0) {
    ctx.fillStyle = '#aaaaaa';
    ctx.font = '13px Inter';
    ctx.textAlign = 'center';
    ctx.fillText('No weight history data available. Log weight to begin.', canvas.width / 2, canvas.height / 2);
    weightChangeDisplay.textContent = '-- kg';
    return;
  }
  
  const firstW = data[0].weight_kg;
  const lastW = data[data.length - 1].weight_kg;
  const delta = lastW - firstW;
  const deltaStr = (delta >= 0 ? '+' : '') + delta.toFixed(1) + ' kg';
  weightChangeDisplay.textContent = deltaStr;
  
  if (delta < 0) {
    weightChangeDisplay.style.color = '#29b6f6'; // loss (blue)
  } else if (delta > 0) {
    weightChangeDisplay.style.color = '#ffa726'; // gain (orange)
  } else {
    weightChangeDisplay.style.color = '#ffffff';
  }
  
  const paddingLeft = 45;
  const paddingRight = 20;
  const paddingTop = 25;
  const paddingBottom = 35;
  
  const graphWidth = canvas.width - paddingLeft - paddingRight;
  const graphHeight = canvas.height - paddingTop - paddingBottom;
  
  const weights = data.map(d => d.weight_kg);
  let minW = Math.min(...weights) - 2;
  let maxW = Math.max(...weights) + 2;
  if (maxW - minW < 4) {
    minW -= 2;
    maxW += 2;
  }
  
  // Draw axes
  ctx.strokeStyle = '#2c2c2c';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(paddingLeft, paddingTop);
  ctx.lineTo(paddingLeft, canvas.height - paddingBottom);
  ctx.lineTo(canvas.width - paddingRight, canvas.height - paddingBottom);
  ctx.stroke();
  
  // Grid Lines & Y labels
  ctx.fillStyle = '#aaaaaa';
  ctx.font = '10px Inter';
  ctx.textAlign = 'right';
  ctx.textBaseline = 'middle';
  
  const subdivisions = 4;
  for (let i = 0; i <= subdivisions; i++) {
    const yVal = minW + (maxW - minW) * (i / subdivisions);
    const yPos = canvas.height - paddingBottom - (i / subdivisions) * graphHeight;
    
    ctx.strokeStyle = '#1f1f1f';
    ctx.beginPath();
    ctx.moveTo(paddingLeft, yPos);
    ctx.lineTo(canvas.width - paddingRight, yPos);
    ctx.stroke();
    
    ctx.fillText(yVal.toFixed(1), paddingLeft - 8, yPos);
  }
  
  // Map coordinates
  const points = [];
  const numPoints = data.length;
  data.forEach((d, idx) => {
    const xPos = paddingLeft + (numPoints > 1 ? (idx / (numPoints - 1)) * graphWidth : graphWidth / 2);
    const yPos = canvas.height - paddingBottom - ((d.weight_kg - minW) / (maxW - minW)) * graphHeight;
    points.push({ x: xPos, y: yPos, date: d.date, weight: d.weight_kg });
  });
  
  // Draw gradient wash area
  if (points.length > 1) {
    ctx.fillStyle = 'rgba(41, 182, 246, 0.07)';
    ctx.beginPath();
    ctx.moveTo(points[0].x, canvas.height - paddingBottom);
    points.forEach(p => {
      ctx.lineTo(p.x, p.y);
    });
    ctx.lineTo(points[points.length - 1].x, canvas.height - paddingBottom);
    ctx.closePath();
    ctx.fill();
  }
  
  // Draw chart connecting line
  ctx.strokeStyle = '#29b6f6';
  ctx.lineWidth = 3;
  ctx.beginPath();
  points.forEach((p, idx) => {
    if (idx === 0) ctx.moveTo(p.x, p.y);
    else ctx.lineTo(p.x, p.y);
  });
  ctx.stroke();
  
  // Build a set of indices that will get date/value labels.
  // Always label the first and last point, then distribute up to
  // MAX_LABELS evenly across the full range so no date is repeated.
  const MAX_LABELS = 5;
  const labelIndices = new Set();
  labelIndices.add(0);
  labelIndices.add(numPoints - 1);
  if (numPoints <= MAX_LABELS) {
    // Show every point when there are few entries
    for (let i = 0; i < numPoints; i++) labelIndices.add(i);
  } else {
    // Evenly space (MAX_LABELS - 2) interior labels between first and last
    const interior = MAX_LABELS - 2;
    for (let k = 1; k <= interior; k++) {
      labelIndices.add(Math.round(k * (numPoints - 1) / (interior + 1)));
    }
  }

  // Draw dots and text
  points.forEach((p, idx) => {
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(p.x, p.y, 4, 0, 2 * Math.PI);
    ctx.fill();
    ctx.strokeStyle = '#29b6f6';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Only label the computed set of indices; each label reads its own p.date
    if (labelIndices.has(idx)) {
      ctx.fillStyle = '#aaaaaa';
      ctx.font = '9px Inter';
      ctx.textAlign = 'center';

      // p.date is "YYYY-MM-DD" from the API; format as MM/DD
      const dateParts = p.date ? p.date.split('-') : [];
      const formattedDate = dateParts.length === 3
        ? `${dateParts[1]}/${dateParts[2]}`
        : (p.date || '');

      ctx.fillText(formattedDate, p.x, canvas.height - paddingBottom + 15);

      ctx.fillStyle = '#ffffff';
      ctx.fillText(p.weight.toFixed(1), p.x, p.y - 10);
    }
  });
}

// Save Quick Weight log
async function saveWeight() {
  const payload = {
    weight_kg: parseFloat(quickWeightInput.value) || 0.0,
    date: quickWeightDate.value
  };

  try {
    const response = await fetch('/weight/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (response.ok) {
      weightModal.classList.remove('active');
      await fetchProfile();
      await refreshDashboard();
    }
  } catch (error) {
    console.error('Error saving weight:', error);
  }
}

// Save Nutrition Log
async function saveFood() {
  const payload = {
    date: foodDate.value,
    calories_consumed: parseFloat(foodCalories.value) || 0.0,
    protein_g: parseFloat(foodProtein.value) || 0.0,
    carbs_g: parseFloat(foodCarbs.value) || 0.0,
    fat_g: parseFloat(foodFat.value) || 0.0
  };

  try {
    const response = await fetch('/nutrition/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (response.ok) {
      foodModal.classList.remove('active');
      await refreshDashboard();
    }
  } catch (error) {
    console.error('Error saving food log:', error);
  }
}

// Estimate Cardio Burn dynamically
function updateCardioEstimate() {
  const metValues = {
    Running: 9.8,
    Cycling: 7.5,
    Swimming: 7.0,
    Walking: 3.5,
    Sports: 8.0,
    Other: 0.0
  };

  const preset = cardioPresetSelect.value;
  let met = metValues[preset];
  if (preset === "Other") {
    met = parseFloat(cardioCustomMet.value) || 5.0;
  }

  const mins = parseFloat(cardioDuration.value) || 0;
  const userWeight = activeProfile ? activeProfile.weight_kg : 75.0;

  // Formula: calories = MET * weight_kg * hours
  const hours = mins / 60.0;
  const cals = met * userWeight * hours;

  cardioEstimatedDisplay.textContent = `${Math.round(cals)} kcal`;
  
  if (!overrideCalorieCheckbox.checked) {
    cardioOverrideVal.value = Math.round(cals);
  }
}

// Save Cardio Log
async function saveCardio() {
  let activity = "";
  let duration = 0.0;
  let calories = 0.0;
  let method = activeCardioTab;

  if (activeCardioTab === "duration") {
    activity = cardioPresetSelect.value;
    duration = parseFloat(cardioDuration.value) || 0.0;
    calories = parseFloat(cardioOverrideVal.value) || 0.0;
  } else {
    activity = cardioActivityName.value || "Cardio Workout";
    duration = parseFloat(cardioDirectDuration.value) || 0.0;
    calories = parseFloat(cardioDirectCalories.value) || 0.0;
    method = "direct_calories";
  }

  const payload = {
    date: cardioDate.value,
    activity_name: activity,
    duration_mins: duration,
    calories_burned: calories,
    entry_method: method
  };

  try {
    const response = await fetch('/cardio/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (response.ok) {
      cardioModal.classList.remove('active');
      await refreshDashboard();
    }
  } catch (error) {
    console.error('Error logging cardio:', error);
  }
}

// Helpers
function getScoreColorClass(score) {
  if (score >= 75) return 'score-green';
  if (score >= 50) return 'score-yellow';
  return 'score-red';
}
function getBarColorClass(score) {
  if (score >= 75) return 'bar-green';
  if (score >= 50) return 'bar-yellow';
  return 'bar-red';
}

// Start streaming workout
async function startWorkout() {
  currentExerciseKey = exerciseSelect.value;
  if (!currentExerciseKey) return;
  
  startBtn.disabled = true;
  exerciseSelect.disabled = true;
  endSetBtn.disabled = false;
  endSessionBtn.disabled = false;
  
  // Set workout start time to track duration
  workoutStartTime = Date.now();
  
  // Set placeholder to opening state
  canvasPlaceholder.style.display = 'flex';
  canvasPlaceholder.innerHTML = `
    <svg class="placeholder-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
      <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z" />
    </svg>
    <p>Opening webcam stream...</p>
  `;
  
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { width: 640, height: 480 }
    });
    video.srcObject = stream;
    video.play();
    canvasPlaceholder.style.display = 'none';
  } catch (error) {
    console.error('Webcam access error:', error);
    
    // Reset controls to idle state
    resetControls();
    
    // Show clear error in placeholder
    canvasPlaceholder.style.display = 'flex';
    canvasPlaceholder.innerHTML = `
      <div style="text-align: center; color: #ff5252; padding: 20px;">
        <svg style="width: 48px; height: 48px; margin-bottom: 12px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
        </svg>
        <p style="font-weight: 600; margin-bottom: 8px;">Webcam Access Denied</p>
        <p style="font-size: 0.9em; color: #aaaaaa; max-width: 300px; margin: 0 auto;">Failed to access camera. Please allow camera permissions in your browser and try again.</p>
      </div>
    `;
    
    // Show error in feedback container
    feedbackContainer.innerHTML = '<div class="feedback-badge badge-red">Webcam access denied. Please verify camera permissions.</div>';
    
    // Update status indicator
    streamStatusEl.textContent = 'Error: Permission Denied';
    streamStatusEl.style.color = '#ff5252';
    
    return;
  }
  
  // Reset status indicator color in case it was colored red previously
  streamStatusEl.style.color = '';
  connectWebSocket();
}

function resetPingTimeout() {
  if (pingTimeout) clearTimeout(pingTimeout);
  pingTimeout = setTimeout(() => {
    console.warn("WebSocket ping timeout - connection lost");
    if (socket) {
      socket.close();
    }
  }, 25000);
}

// Connect websocket
function connectWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${window.location.host}/ws/workout`;
  
  socket = new WebSocket(wsUrl);
  
  socket.onopen = () => {
    streamStatusEl.textContent = 'Connected';
    streamStatusEl.classList.add('connected');
    streamStatusEl.classList.remove('tracking');
    isSending = true;
    startFrameLoop();
    resetPingTimeout();
  };
  
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === 'ping') {
      socket.send(JSON.stringify({ type: 'pong' }));
      resetPingTimeout();
      return;
    }
    
    // Draw frame
    if (data.frame) {
      const img = new Image();
      img.onload = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      };
      img.src = `data:image/jpeg;base64,${data.frame}`;
    }
    
    lastRepsCounted = data.reps;
    lastAvgFormScore = data.form_score;
    
    // Format hold vs rep displays
    if (isHoldMode) {
      const mins = Math.floor(data.reps / 60);
      const secs = data.reps % 60;
      repCountEl.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    } else {
      repCountEl.textContent = data.reps;
    }
    
    stageLabelEl.textContent = data.stage || '--';
    
    formScorePercentEl.textContent = `${Math.round(data.form_score)}%`;
    formScorePercentEl.className = getScoreColorClass(data.form_score);
    formScoreBarEl.className = `progress-bar ${getBarColorClass(data.form_score)}`;
    formScoreBarEl.style.width = `${Math.max(5, data.form_score)}%`;
    
    // Update feedback
    feedbackContainer.innerHTML = '';
    if (data.feedback && data.feedback.length > 0) {
      data.feedback.slice(-3).forEach(fb => {
        const badge = document.createElement('div');
        badge.className = `feedback-badge ${getBadgeClass(fb.severity)}`;
        badge.textContent = fb.message;
        feedbackContainer.appendChild(badge);
      });
    } else {
      feedbackContainer.innerHTML = `<div class="feedback-badge badge-green">${isHoldMode ? 'Holding alignment...' : 'Performing rep...'}</div>`;
    }
    
    // Update angles
    anglesContainer.innerHTML = '';
    if (data.angles && Object.keys(data.angles).length > 0) {
      Object.keys(data.angles).forEach(joint => {
        const angleVal = Math.round(data.angles[joint]);
        const angleDiv = document.createElement('div');
        angleDiv.className = 'angle-badge';
        angleDiv.innerHTML = `
          <span class="angle-name">${joint.replace('_', ' ')}</span>
          <span class="angle-val">${angleVal}°</span>
        `;
        anglesContainer.appendChild(angleDiv);
      });
      streamStatusEl.textContent = 'Tracking Pose';
      streamStatusEl.classList.add('tracking');
    } else {
      anglesContainer.innerHTML = '<span class="angle-item-placeholder">No pose detected</span>';
      streamStatusEl.textContent = 'Connected';
      streamStatusEl.classList.remove('tracking');
    }
  };
  
  socket.onclose = () => {
    if (pingTimeout) {
      clearTimeout(pingTimeout);
      pingTimeout = null;
    }
    streamStatusEl.classList.remove('connected', 'tracking');
    stopFrameLoop();
    
    if (isSending) {
      // Connection dropped mid-set. Attempt reconnect with a visible status indicator.
      streamStatusEl.textContent = 'Reconnecting...';
      streamStatusEl.style.color = '#ffa726'; // amber warning color
      
      if (!reconnectTimer) {
        reconnectTimer = setTimeout(() => {
          reconnectTimer = null;
          connectWebSocket();
        }, 2000);
      }
    } else {
      streamStatusEl.textContent = 'Disconnected';
      streamStatusEl.style.color = '';
      isSending = false;
    }
  };
}

function getBadgeClass(severity) {
  if (severity === 'RED') return 'badge-red';
  if (severity === 'YELLOW') return 'badge-yellow';
  return 'badge-green';
}

function startFrameLoop() {
  if (sendInterval) clearInterval(sendInterval);
  
  sendInterval = setInterval(() => {
    if (!isSending || !socket || socket.readyState !== WebSocket.OPEN) return;
    
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = 640;
    tempCanvas.height = 480;
    const tempCtx = tempCanvas.getContext('2d');
    tempCtx.drawImage(video, 0, 0, 640, 480);
    
    const base64Data = tempCanvas.toDataURL('image/jpeg', 0.7);
    
    const payload = {
      frame: base64Data,
      exercise: currentExerciseKey,
      current_reps: lastRepsCounted
    };
    
    socket.send(JSON.stringify(payload));
  }, 100);
}

function stopFrameLoop() {
  if (sendInterval) {
    clearInterval(sendInterval);
    sendInterval = null;
  }
}

// Trigger end of a set
function endSet() {
  isSending = false;
  if (socket) {
    socket.close();
  }
  
  // Calculate exact set duration
  const durationSeconds = (Date.now() - workoutStartTime) / 1000.0;
  
  const exName = exerciseSelect.options[exerciseSelect.selectedIndex].text;
  modalExercise.value = exName;
  
  if (isHoldMode) {
    modalRepsLabel.textContent = "Hold Time (sec)";
    modalReps.value = lastRepsCounted;
  } else {
    modalRepsLabel.textContent = "Reps";
    modalReps.value = lastRepsCounted;
  }
  
  modalScore.value = `${Math.round(lastAvgFormScore)}%`;
  
  weightInput.value = 0;
  weightModeSelect.value = "total";
  setDurationInput.value = "";
  rpeInput.value = 7;
  rpeValue.textContent = 7;
  painCheckbox.checked = false;
  painLocationGroup.style.display = 'none';
  painLocationInput.value = '';
  
  // Store computed duration on saveSetBtn data attribute
  saveSetBtn.setAttribute('data-duration', durationSeconds);
  
  logSetModal.classList.add('active');
}

// Discard Set
function discardSet() {
  if (reconnectTimer) {
    clearTimeout(reconnectTimer);
    reconnectTimer = null;
  }
  logSetModal.classList.remove('active');
  resetSetStats();
  workoutStartTime = Date.now();
  connectWebSocket();
}

function resetSetStats() {
  lastRepsCounted = 0;
  lastAvgFormScore = 100;
  repCountEl.textContent = isHoldMode ? '00:00' : '0';
  stageLabelEl.textContent = '--';
  formScorePercentEl.textContent = '100%';
  formScorePercentEl.className = 'score-green';
  formScoreBarEl.className = 'progress-bar bar-green';
  formScoreBarEl.style.width = '100%';
  feedbackContainer.innerHTML = '<div class="feedback-badge badge-green">Ready for next set!</div>';
  anglesContainer.innerHTML = '<span class="angle-item-placeholder">No pose detected</span>';
}

// Save Set details
async function saveSet() {
  const reps = parseInt(modalReps.value);
  const repsCounted = isNaN(reps) ? lastRepsCounted : reps;
  
  let duration = parseFloat(setDurationInput.value);
  if (isNaN(duration)) {
    duration = parseFloat(saveSetBtn.getAttribute('data-duration')) || 0.0;
  }
  
  const payload = {
    session_id: currentSessionId,
    exercise_key: currentExerciseKey,
    set_number: currentSetNumber,
    reps_counted: repsCounted,
    weight_kg: parseFloat(weightInput.value) || 0,
    weight_mode: weightModeSelect.value || "total",
    rpe: parseInt(rpeInput.value),
    avg_form_score: lastAvgFormScore,
    pain_flag: painCheckbox.checked,
    pain_location: painCheckbox.checked ? painLocationInput.value : "",
    duration_seconds: duration
  };
  
  try {
    const response = await fetch('/set/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    if (response.ok) {
      const resData = await response.json();
      if (resData && resData.session_id) {
        currentSessionId = resData.session_id;
      }
      currentSetNumber++;
      
      sessionSets++;
      sessionReps += repsCounted;
      if (sessionSets === 1) {
        sessionAvgScore = lastAvgFormScore;
      } else {
        sessionAvgScore = (sessionAvgScore * (sessionSets - 1) + lastAvgFormScore) / sessionSets;
      }
      
      logSetModal.classList.remove('active');
      resetSetStats();
      workoutStartTime = Date.now();
      connectWebSocket();
      await refreshDashboard();
    } else {
      const err = await response.json();
      alert(`Error saving set: ${err.detail || 'Unknown error'}`);
    }
  } catch (error) {
    console.error('Error logging set:', error);
  }
}

// End current session
async function endSession() {
  isSending = false;
  if (reconnectTimer) {
    clearTimeout(reconnectTimer);
    reconnectTimer = null;
  }
  stopFrameLoop();
  if (socket) {
    socket.close();
  }
  
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
    stream = null;
  }
  
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  canvasPlaceholder.style.display = 'flex';
  
  sumSetsEl.textContent = sessionSets;
  if (isHoldMode) {
    sumRepsLabel.textContent = "Hold Time";
    const mins = Math.floor(sessionReps / 60);
    const secs = sessionReps % 60;
    sumRepsEl.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  } else {
    sumRepsLabel.textContent = "Reps";
    sumRepsEl.textContent = sessionReps;
  }
  
  sumScoreEl.textContent = `${Math.round(sessionAvgScore)}%`;
  sessionNotes.value = '';
  
  // Calculate dynamic calories using MET value * latest weight
  let totalCals = 0.0;
  try {
    // We fetch a list of session calories or compute it from active session in DB
    const recentRes = await fetch('/sessions/recent');
    if (recentRes.ok) {
      const recents = await recentRes.json();
      // Since our active session is logged in db, let's display calories in summary modal
      // We can get details of the current session in progress before saving
    }
  } catch (e) {}
  
  // Default display
  sumCaloriesEl.textContent = "--";
  
  summaryModal.classList.add('active');
}

// Save completed session details
async function saveSession() {
  const payload = {
    session_id: currentSessionId,
    notes: sessionNotes.value
  };
  
  try {
    const response = await fetch('/session/end', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    if (response.ok) {
      summaryModal.classList.remove('active');
      resetControls();
      await fetchRecentSessions();
      await refreshDashboard();
    } else {
      alert('Error finalizing session.');
    }
  } catch (error) {
    console.error('Error saving session:', error);
  }
}

// Restore controls state to idle
function resetControls() {
  startBtn.disabled = false;
  exerciseSelect.disabled = false;
  endSetBtn.disabled = true;
  endSessionBtn.disabled = true;
  
  currentSessionId = null;
  currentSetNumber = 1;
  sessionSets = 0;
  sessionReps = 0;
  sessionAvgScore = 100;
  
  resetSetStats();
}
