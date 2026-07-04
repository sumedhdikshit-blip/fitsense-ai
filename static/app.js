// FitSense AI Frontend Logic

let stream = null;
let socket = null;
let sendInterval = null;
let isSending = false;

// Workout session states
let currentExerciseKey = "";
let currentSetNumber = 1;
let lastRepsCounted = 0;
let lastAvgFormScore = 100;
let sessionSets = 0;
let sessionReps = 0;
let sessionAvgScore = 100;

// DOM Elements
const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const canvasPlaceholder = document.getElementById('canvasPlaceholder');

const exerciseSelect = document.getElementById('exerciseSelect');
const startBtn = document.getElementById('startBtn');
const endSetBtn = document.getElementById('endSetBtn');
const endSessionBtn = document.getElementById('endSessionBtn');

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
const modalScore = document.getElementById('modalScore');
const weightInput = document.getElementById('weightInput');
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
const sumScoreEl = document.getElementById('sumScore');
const sessionNotes = document.getElementById('sessionNotes');
const saveSessionBtn = document.getElementById('saveSessionBtn');

// Session Detail Modal Elements
const detailModal = document.getElementById('detailModal');
const closeDetailBtn = document.getElementById('closeDetailBtn');
const detailTitle = document.getElementById('detailTitle');
const detDate = document.getElementById('detDate');
const detDuration = document.getElementById('detDuration');
const detForm = document.getElementById('detForm');
const detNotes = document.getElementById('detNotes');
const detailSetsBody = document.getElementById('detailSetsBody');

const historyBody = document.getElementById('historyBody');

// Initialization
document.addEventListener('DOMContentLoaded', () => {
  fetchExercises();
  fetchRecentSessions();
  setupEventListeners();
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
}

// Fetch exercises from config endpoint
async function fetchExercises() {
  try {
    const response = await fetch('/exercises');
    const exercises = await response.json();
    
    exerciseSelect.innerHTML = '';
    
    // Group exercises by category for aesthetics
    const categories = {
      lower_body: 'Lower Body',
      upper_body: 'Upper Body',
      core: 'Core',
      cardio: 'Cardio',
      full_body: 'Full Body'
    };
    
    // Create option groups
    Object.keys(categories).forEach(catKey => {
      const catEx = exercises.filter(ex => ex.category === catKey);
      if (catEx.length > 0) {
        const group = document.createElement('optgroup');
        group.label = categories[catKey];
        catEx.forEach(ex => {
          const opt = document.createElement('option');
          opt.value = ex.key;
          opt.textContent = ex.display_name;
          group.appendChild(opt);
        });
        exerciseSelect.appendChild(group);
      }
    });
    
    startBtn.disabled = false;
  } catch (error) {
    console.error('Error fetching exercises:', error);
    exerciseSelect.innerHTML = '<option value="" disabled>Error loading exercises</option>';
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
          <td colspan="6" style="text-align: center; color: #aaaaaa;">No workout history found. Log a session to get started.</td>
        </tr>
      `;
      return;
    }
    
    historyBody.innerHTML = '';
    sessions.forEach(sess => {
      const dateFormatted = new Date(sess.date).toLocaleDateString(undefined, {
        year: 'numeric', month: 'short', day: 'numeric'
      });
      
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${dateFormatted}</td>
        <td>${sess.exercises_done || 'None'}</td>
        <td>${sess.total_sets}</td>
        <td>${sess.total_reps}</td>
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
    detForm.textContent = Math.round(detail.avg_form_score);
    detNotes.textContent = detail.notes || 'No notes added.';
    
    detailSetsBody.innerHTML = '';
    if (detail.exercises) {
      detail.exercises.forEach(ex => {
        if (ex.sets) {
          ex.sets.forEach(set => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
              <td>Set ${set.set_number}</td>
              <td><strong>${ex.exercise_name}</strong></td>
              <td>${set.reps_counted}</td>
              <td>${set.weight_kg} kg</td>
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

// Helper color class
function getScoreColorClass(score) {
  if (score >= 75) return 'score-green';
  if (score >= 50) return 'score-yellow';
  return 'score-red';
}

// Helper bar color class
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
  
  // Set up camera
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: { width: 640, height: 480 }
    });
    video.srcObject = stream;
    video.play();
    canvasPlaceholder.style.display = 'none';
  } catch (error) {
    console.error('Webcam access error:', error);
    alert('Failed to access webcam. Please verify camera permissions.');
    resetControls();
    return;
  }
  
  connectWebSocket();
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
  };
  
  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    // 1. Draw annotated frame
    if (data.frame) {
      const img = new Image();
      img.onload = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
      };
      img.src = `data:image/jpeg;base64,${data.frame}`;
    }
    
    // 2. Update real-time stats
    lastRepsCounted = data.reps;
    lastAvgFormScore = data.form_score;
    
    repCountEl.textContent = data.reps;
    stageLabelEl.textContent = data.stage || '--';
    
    // Update score bar
    formScorePercentEl.textContent = `${Math.round(data.form_score)}%`;
    formScorePercentEl.className = getScoreColorClass(data.form_score);
    formScoreBarEl.className = `progress-bar ${getBarColorClass(data.form_score)}`;
    formScoreBarEl.style.width = `${Math.max(5, data.form_score)}%`;
    
    // Update feedback list
    feedbackContainer.innerHTML = '';
    if (data.feedback && data.feedback.length > 0) {
      // slice to latest 3
      data.feedback.slice(-3).forEach(fb => {
        const badge = document.createElement('div');
        badge.className = `feedback-badge ${getBadgeClass(fb.severity)}`;
        badge.textContent = fb.message;
        feedbackContainer.appendChild(badge);
      });
    } else {
      feedbackContainer.innerHTML = '<div class="feedback-badge badge-green">Performing rep...</div>';
    }
    
    // Update live joint angles
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
    streamStatusEl.textContent = 'Disconnected';
    streamStatusEl.classList.remove('connected', 'tracking');
    isSending = false;
    stopFrameLoop();
  };
  
  socket.onerror = (err) => {
    console.error('WebSocket Error:', err);
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
    
    // Draw hidden video to canvas to capture frame
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = 640;
    tempCanvas.height = 480;
    const tempCtx = tempCanvas.getContext('2d');
    tempCtx.drawImage(video, 0, 0, 640, 480);
    
    const base64Data = tempCanvas.toDataURL('image/jpeg', 0.7);
    
    const payload = {
      frame: base64Data,
      exercise: currentExerciseKey
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
  // 1. Pause frame streaming
  isSending = false;
  if (socket) {
    socket.close();
  }
  
  // 2. Open Log Set Modal with prefilled values
  const exName = exerciseSelect.options[exerciseSelect.selectedIndex].text;
  modalExercise.value = exName;
  modalReps.value = lastRepsCounted;
  modalScore.value = `${Math.round(lastAvgFormScore)}%`;
  
  // Reset inputs
  weightInput.value = 0;
  rpeInput.value = 7;
  rpeValue.textContent = 7;
  painCheckbox.checked = false;
  painLocationGroup.style.display = 'none';
  painLocationInput.value = '';
  
  logSetModal.classList.add('active');
}

// Discard/Cancel Set
function discardSet() {
  logSetModal.classList.remove('active');
  resetSetStats();
  
  // Resume streaming (new set connection)
  connectWebSocket();
}

function resetSetStats() {
  lastRepsCounted = 0;
  lastAvgFormScore = 100;
  repCountEl.textContent = '0';
  stageLabelEl.textContent = '--';
  formScorePercentEl.textContent = '100%';
  formScorePercentEl.className = 'score-green';
  formScoreBarEl.className = 'progress-bar bar-green';
  formScoreBarEl.style.width = '100%';
  feedbackContainer.innerHTML = '<div class="feedback-badge badge-green">Ready for next set!</div>';
  anglesContainer.innerHTML = '<span class="angle-item-placeholder">No pose detected</span>';
}

// Save Set details to backend
async function saveSet() {
  const payload = {
    exercise_key: currentExerciseKey,
    set_number: currentSetNumber,
    reps_counted: lastRepsCounted,
    weight_kg: parseFloat(weightInput.value) || 0,
    rpe: parseInt(rpeInput.value),
    avg_form_score: lastAvgFormScore,
    pain_flag: painCheckbox.checked,
    pain_location: painCheckbox.checked ? painLocationInput.value : ""
  };
  
  try {
    const response = await fetch('/set/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    
    if (response.ok) {
      currentSetNumber++;
      
      // Update session totals for display
      sessionSets++;
      sessionReps += lastRepsCounted;
      // Running average of form score
      if (sessionSets === 1) {
        sessionAvgScore = lastAvgFormScore;
      } else {
        sessionAvgScore = (sessionAvgScore * (sessionSets - 1) + lastAvgFormScore) / sessionSets;
      }
      
      logSetModal.classList.remove('active');
      resetSetStats();
      
      // Resume streaming (starts new set connection)
      connectWebSocket();
    } else {
      const err = await response.json();
      alert(`Error saving set: ${err.detail || 'Unknown error'}`);
    }
  } catch (error) {
    console.error('Error logging set:', error);
    alert('Network error saving set.');
  }
}

// End current session
function endSession() {
  // Pause frame stream
  isSending = false;
  stopFrameLoop();
  if (socket) {
    socket.close();
  }
  
  // Close camera
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
    stream = null;
  }
  
  // Reset canvas visualization
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  canvasPlaceholder.style.display = 'flex';
  
  // Populate summary modal values
  sumSetsEl.textContent = sessionSets;
  sumRepsEl.textContent = sessionReps;
  sumScoreEl.textContent = `${Math.round(sessionAvgScore)}%`;
  sessionNotes.value = '';
  
  summaryModal.classList.add('active');
}

// Save completed session details to backend
async function saveSession() {
  const payload = {
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
      
      // Reset full workout state
      resetControls();
      
      // Refresh session lists
      fetchRecentSessions();
    } else {
      alert('Error finalizing session.');
    }
  } catch (error) {
    console.error('Error saving session:', error);
    alert('Network error saving session.');
  }
}

// Restore controls state to idle
function resetControls() {
  startBtn.disabled = false;
  exerciseSelect.disabled = false;
  endSetBtn.disabled = true;
  endSessionBtn.disabled = true;
  
  currentSetNumber = 1;
  sessionSets = 0;
  sessionReps = 0;
  sessionAvgScore = 100;
  
  resetSetStats();
}
