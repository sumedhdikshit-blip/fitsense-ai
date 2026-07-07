// FitSense AI — Workout Page Logic

let stream = null;
let socket = null;
let sendInterval = null;
let isSending = false;
let reconnectTimer = null;
let pingTimeout = null;
let reconnectAttempts = 0;
let currentReconnectDelay = 1000; // start at 1s

let currentExerciseKey = '';
let currentSetNumber = 1;
let lastRepsCounted = 0;
let lastAvgFormScore = 100;
let sessionSets = 0;
let sessionReps = 0;
let sessionAvgScore = 100;
let currentSessionId = null;
let isHoldMode = false;
let workoutStartTime = 0;
let captureCanvas = null;

// DOM refs (filled after DOMContentLoaded)
let video, canvas, ctx, canvasPlaceholder;
let exerciseSelect, startBtn, endSetBtn, endSessionBtn;
let repLabelEl, repCountEl, stageLabelEl, formScorePercentEl, formScoreBarEl;
let feedbackContainer, anglesContainer, streamStatusEl;
let logSetModal, modalExercise, modalReps, modalRepsLabel, modalScore;
let weightInput, weightModeSelect, setDurationInput, rpeInput, rpeValue;
let painCheckbox, painLocationGroup, painLocationInput, saveSetBtn, cancelSetBtn;
let summaryModal, sumSetsEl, sumRepsEl, sumRepsLabel, sumCaloriesEl, sumScoreEl;
let sessionNotes, saveSessionBtn;

document.addEventListener('DOMContentLoaded', async () => {
  injectNav('workout');
  const user = await initAuth();
  if (!user) return;

  await fetchProfile();
  bindDomRefs();
  setupEventListeners();
  await fetchExercises();
});

function bindDomRefs() {
  video = document.getElementById('video');
  canvas = document.getElementById('canvas');
  ctx = canvas.getContext('2d');
  canvasPlaceholder = document.getElementById('canvasPlaceholder');

  exerciseSelect = document.getElementById('exerciseSelect');
  startBtn       = document.getElementById('startBtn');
  endSetBtn      = document.getElementById('endSetBtn');
  endSessionBtn  = document.getElementById('endSessionBtn');

  repLabelEl          = document.getElementById('repLabel');
  repCountEl          = document.getElementById('repCount');
  stageLabelEl        = document.getElementById('stageLabel');
  formScorePercentEl  = document.getElementById('formScorePercent');
  formScoreBarEl      = document.getElementById('formScoreBar');
  feedbackContainer   = document.getElementById('feedbackContainer');
  anglesContainer     = document.getElementById('anglesContainer');
  streamStatusEl      = document.getElementById('streamStatus');

  logSetModal      = document.getElementById('logSetModal');
  modalExercise    = document.getElementById('modalExercise');
  modalReps        = document.getElementById('modalReps');
  modalRepsLabel   = document.getElementById('modalRepsLabel');
  modalScore       = document.getElementById('modalScore');
  weightInput      = document.getElementById('weightInput');
  weightModeSelect = document.getElementById('weightModeSelect');
  setDurationInput = document.getElementById('setDurationInput');
  rpeInput         = document.getElementById('rpeInput');
  rpeValue         = document.getElementById('rpeValue');
  painCheckbox     = document.getElementById('painCheckbox');
  painLocationGroup = document.getElementById('painLocationGroup');
  painLocationInput = document.getElementById('painLocationInput');
  saveSetBtn       = document.getElementById('saveSetBtn');
  cancelSetBtn     = document.getElementById('cancelSetBtn');

  summaryModal    = document.getElementById('summaryModal');
  sumSetsEl       = document.getElementById('sumSets');
  sumRepsEl       = document.getElementById('sumReps');
  sumRepsLabel    = document.getElementById('sumRepsLabel');
  sumCaloriesEl   = document.getElementById('sumCalories');
  sumScoreEl      = document.getElementById('sumScore');
  sessionNotes    = document.getElementById('sessionNotes');
  saveSessionBtn  = document.getElementById('saveSessionBtn');
}

function setupEventListeners() {
  startBtn.addEventListener('click', startWorkout);
  endSetBtn.addEventListener('click', endSet);
  endSessionBtn.addEventListener('click', endSession);

  // Manual entry
  const logManualBtn = document.getElementById('logManualBtn');
  logManualBtn.addEventListener('click', openManualEntryModal);
  document.getElementById('closeManualBtn').addEventListener('click', closeManualEntryModal);
  document.getElementById('cancelManualBtn').addEventListener('click', closeManualEntryModal);
  document.getElementById('saveManualBtn').addEventListener('click', saveManualEntry);
  document.getElementById('manualRpeInput').addEventListener('input', (e) => {
    document.getElementById('manualRpeValue').textContent = e.target.value;
  });

  painCheckbox.addEventListener('change', (e) => {
    painLocationGroup.style.display = e.target.checked ? 'flex' : 'none';
  });
  rpeInput.addEventListener('input', (e) => { rpeValue.textContent = e.target.value; });

  saveSetBtn.addEventListener('click', saveSet);
  cancelSetBtn.addEventListener('click', discardSet);
  saveSessionBtn.addEventListener('click', saveSession);

  exerciseSelect.addEventListener('change', () => {
    const opt = exerciseSelect.options[exerciseSelect.selectedIndex];
    isHoldMode = opt.getAttribute('data-mode') === 'hold';
    repLabelEl.textContent = isHoldMode ? 'HOLD TIME' : 'REPS';
  });
}

async function fetchExercises() {
  try {
    const res = await fetch('/exercises');
    const exercises = await res.json();

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

    if (exerciseSelect.options.length > 0) {
      isHoldMode = exerciseSelect.options[0].getAttribute('data-mode') === 'hold';
      repLabelEl.textContent = isHoldMode ? 'HOLD TIME' : 'REPS';
    }
    startBtn.disabled = false;
  } catch (e) {
    console.error('fetchExercises error:', e);
  }
}

async function startWorkout() {
  currentExerciseKey = exerciseSelect.value;
  if (!currentExerciseKey) return;

  startBtn.disabled = true;
  exerciseSelect.disabled = true;
  endSetBtn.disabled = false;
  endSessionBtn.disabled = false;
  workoutStartTime = Date.now();

  canvasPlaceholder.style.display = 'flex';
  canvasPlaceholder.innerHTML = `
    <svg class="placeholder-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
      <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z" />
    </svg>
    <p>Opening webcam stream...</p>
  `;

  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
    video.srcObject = stream;
    video.play();
    canvasPlaceholder.style.display = 'none';
  } catch (error) {
    console.error('Webcam access error:', error);
    resetControls();
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
    feedbackContainer.innerHTML = '<div class="feedback-badge badge-red">Webcam access denied. Please verify camera permissions.</div>';
    streamStatusEl.textContent = 'Error: Permission Denied';
    streamStatusEl.style.color = '#ff5252';
    return;
  }

  streamStatusEl.style.color = '';
  connectWebSocket();
}

function resetPingTimeout() {
  if (pingTimeout) clearTimeout(pingTimeout);
  pingTimeout = setTimeout(() => {
    console.warn('WebSocket ping timeout');
    if (socket) socket.close();
  }, 25000);
}

function connectWebSocket() {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  socket = new WebSocket(`${protocol}//${window.location.host}/ws/workout`);

  socket.onopen = () => {
    reconnectAttempts = 0;
    currentReconnectDelay = 1000;
    streamStatusEl.textContent = 'Connected';
    streamStatusEl.classList.add('connected');
    streamStatusEl.classList.remove('tracking');
    isSending = true;
    startFrameLoop();
    resetPingTimeout();
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'ping') { socket.send(JSON.stringify({ type: 'pong' })); resetPingTimeout(); return; }

    if (data.frame) {
      const img = new Image();
      img.onload = () => { ctx.clearRect(0, 0, canvas.width, canvas.height); ctx.drawImage(img, 0, 0, canvas.width, canvas.height); };
      img.src = `data:image/jpeg;base64,${data.frame}`;
    }

    lastRepsCounted = data.reps;
    lastAvgFormScore = data.form_score;

    if (isHoldMode) {
      const mins = Math.floor(data.reps / 60), secs = data.reps % 60;
      repCountEl.textContent = `${String(mins).padStart(2,'0')}:${String(secs).padStart(2,'0')}`;
    } else {
      repCountEl.textContent = data.reps;
    }

    stageLabelEl.textContent = data.stage || '--';
    formScorePercentEl.textContent = `${Math.round(data.form_score)}%`;
    formScorePercentEl.className = getScoreColorClass(data.form_score);
    formScoreBarEl.className = `progress-bar ${getBarColorClass(data.form_score)}`;
    formScoreBarEl.style.width = `${Math.max(5, data.form_score)}%`;

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

    anglesContainer.innerHTML = '';
    if (data.angles && Object.keys(data.angles).length > 0) {
      Object.keys(data.angles).forEach(joint => {
        const div = document.createElement('div');
        div.className = 'angle-badge';
        div.innerHTML = `<span class="angle-name">${joint.replace('_', ' ')}</span><span class="angle-val">${Math.round(data.angles[joint])}°</span>`;
        anglesContainer.appendChild(div);
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
    if (pingTimeout) { clearTimeout(pingTimeout); pingTimeout = null; }
    streamStatusEl.classList.remove('connected', 'tracking');
    stopFrameLoop();
    if (isSending) {
      if (reconnectAttempts >= 10) {
        streamStatusEl.textContent = 'Connection lost, please refresh';
        streamStatusEl.style.color = '#ef5350';
        isSending = false;
        return;
      }
      streamStatusEl.textContent = `Reconnecting... (Attempt ${reconnectAttempts + 1}/10)`;
      streamStatusEl.style.color = '#ffa726';
      if (!reconnectTimer) {
        reconnectTimer = setTimeout(() => {
          reconnectTimer = null;
          reconnectAttempts++;
          currentReconnectDelay = Math.min(30000, currentReconnectDelay * 2);
          connectWebSocket();
        }, currentReconnectDelay);
      }
    } else {
      streamStatusEl.textContent = 'Disconnected';
      streamStatusEl.style.color = '';
      isSending = false;
    }
  };
}

function startFrameLoop() {
  if (sendInterval) clearInterval(sendInterval);
  
  if (!captureCanvas) {
    captureCanvas = document.createElement('canvas');
    captureCanvas.width = 640;
    captureCanvas.height = 480;
  }
  const captureCtx = captureCanvas.getContext('2d');
  
  sendInterval = setInterval(() => {
    if (!isSending || !socket || socket.readyState !== WebSocket.OPEN) return;
    captureCtx.drawImage(video, 0, 0, 640, 480);
    socket.send(JSON.stringify({ frame: captureCanvas.toDataURL('image/jpeg', 0.7), exercise: currentExerciseKey, current_reps: lastRepsCounted }));
  }, 100);
}

function stopFrameLoop() {
  if (sendInterval) { clearInterval(sendInterval); sendInterval = null; }
}

function endSet() {
  isSending = false;
  if (socket) socket.close();
  const durationSeconds = (Date.now() - workoutStartTime) / 1000.0;
  const exName = exerciseSelect.options[exerciseSelect.selectedIndex].text;
  modalExercise.value = exName;
  modalRepsLabel.textContent = isHoldMode ? 'Hold Time (sec)' : 'Reps';
  modalReps.value = lastRepsCounted;
  modalScore.value = `${Math.round(lastAvgFormScore)}%`;
  weightInput.value = 0;
  weightModeSelect.value = 'total';
  setDurationInput.value = '';
  rpeInput.value = 7;
  rpeValue.textContent = 7;
  painCheckbox.checked = false;
  painLocationGroup.style.display = 'none';
  painLocationInput.value = '';
  saveSetBtn.setAttribute('data-duration', durationSeconds);
  logSetModal.classList.add('active');
}

function discardSet() {
  if (reconnectTimer) { clearTimeout(reconnectTimer); reconnectTimer = null; }
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

async function saveSet() {
  const reps = parseInt(modalReps.value);
  const repsCounted = isNaN(reps) ? lastRepsCounted : reps;
  let duration = parseFloat(setDurationInput.value);
  if (isNaN(duration)) duration = parseFloat(saveSetBtn.getAttribute('data-duration')) || 0.0;

  const payload = {
    session_id: currentSessionId,
    exercise_key: currentExerciseKey,
    set_number: currentSetNumber,
    reps_counted: repsCounted,
    weight_kg: parseFloat(weightInput.value) || 0,
    weight_mode: weightModeSelect.value || 'total',
    rpe: parseInt(rpeInput.value),
    avg_form_score: lastAvgFormScore,
    pain_flag: painCheckbox.checked,
    pain_location: painCheckbox.checked ? painLocationInput.value : '',
    duration_seconds: duration
  };

  try {
    const res = await fetch('/set/log', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    if (res.ok) {
      const resData = await res.json();
      if (resData && resData.session_id) currentSessionId = resData.session_id;
      currentSetNumber++;
      sessionSets++;
      sessionReps += repsCounted;
      sessionAvgScore = sessionSets === 1 ? lastAvgFormScore : (sessionAvgScore * (sessionSets - 1) + lastAvgFormScore) / sessionSets;
      logSetModal.classList.remove('active');
      resetSetStats();
      workoutStartTime = Date.now();
      connectWebSocket();
    } else {
      const err = await res.json();
      alert(`Error saving set: ${err.detail || 'Unknown error'}`);
    }
  } catch (e) { console.error('saveSet error:', e); }
}

async function endSession() {
  isSending = false;
  if (reconnectTimer) { clearTimeout(reconnectTimer); reconnectTimer = null; }
  stopFrameLoop();
  if (socket) socket.close();
  if (stream) { stream.getTracks().forEach(t => t.stop()); stream = null; }

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  canvasPlaceholder.style.display = 'flex';

  sumSetsEl.textContent = sessionSets;
  if (isHoldMode) {
    sumRepsLabel.textContent = 'Hold Time';
    const mins = Math.floor(sessionReps / 60), secs = sessionReps % 60;
    sumRepsEl.textContent = `${String(mins).padStart(2,'0')}:${String(secs).padStart(2,'0')}`;
  } else {
    sumRepsLabel.textContent = 'Reps';
    sumRepsEl.textContent = sessionReps;
  }
  sumScoreEl.textContent = `${Math.round(sessionAvgScore)}%`;
  sumCaloriesEl.textContent = '--';
  sessionNotes.value = '';
  summaryModal.classList.add('active');
}

async function saveSession() {
  const payload = { session_id: currentSessionId, notes: sessionNotes.value };
  try {
    const res = await fetch('/session/end', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    if (res.ok) {
      summaryModal.classList.remove('active');
      resetControls();
    } else {
      alert('Error finalizing session.');
    }
  } catch (e) { console.error('saveSession error:', e); }
}

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

// ── Manual Entry ───────────────────────────────────────────────────────────

function openManualEntryModal() {
  // Populate the manual exercise dropdown from the same source as the camera dropdown
  const manualSel = document.getElementById('manualExerciseSelect');
  if (exerciseSelect && exerciseSelect.children.length > 0 && manualSel.children.length <= 1) {
    // Mirror the camera dropdown options (already grouped by category)
    manualSel.innerHTML = '';
    Array.from(exerciseSelect.children).forEach(child => {
      manualSel.appendChild(child.cloneNode(true));
    });
  }

  // Reset fields
  document.getElementById('manualSetsCount').value = 3;
  document.getElementById('manualRepsCount').value = 10;
  document.getElementById('manualWeightInput').value = 0;
  document.getElementById('manualWeightMode').value = 'total';
  document.getElementById('manualDuration').value = '';
  document.getElementById('manualRpeInput').value = 7;
  document.getElementById('manualRpeValue').textContent = 7;
  document.getElementById('manualSessionNotes').value = '';
  const statusEl = document.getElementById('manualSaveStatus');
  statusEl.style.display = 'none';
  statusEl.textContent = '';

  const saveBtn = document.getElementById('saveManualBtn');
  saveBtn.disabled = false;
  saveBtn.textContent = 'Save All Sets';

  document.getElementById('manualEntryModal').classList.add('active');
}

function closeManualEntryModal() {
  document.getElementById('manualEntryModal').classList.remove('active');
}

async function saveManualEntry() {
  const exerciseKey = document.getElementById('manualExerciseSelect').value;
  if (!exerciseKey) {
    alert('Please select an exercise.');
    return;
  }

  const setsCount   = parseInt(document.getElementById('manualSetsCount').value) || 1;
  const repsPerSet  = parseInt(document.getElementById('manualRepsCount').value) || 0;
  const weight      = parseFloat(document.getElementById('manualWeightInput').value) || 0.0;
  const weightMode  = document.getElementById('manualWeightMode').value;   // 'total' | 'per_side' — stored verbatim
  const durSec      = parseFloat(document.getElementById('manualDuration').value) || 0.0;
  const rpe         = parseInt(document.getElementById('manualRpeInput').value) || 7;
  const notes       = document.getElementById('manualSessionNotes').value.trim();

  const saveBtn  = document.getElementById('saveManualBtn');
  const statusEl = document.getElementById('manualSaveStatus');
  saveBtn.disabled = true;
  saveBtn.textContent = 'Saving...';
  statusEl.style.display = 'none';

  try {
    // Create a fresh session for this manual entry
    let manualSessionId = null;

    for (let i = 1; i <= setsCount; i++) {
      const payload = {
        session_id:    manualSessionId,   // null on first call → backend creates session
        exercise_key:  exerciseKey,
        set_number:    i,
        reps_counted:  repsPerSet,
        weight_kg:     weight,
        weight_mode:   weightMode,        // stored exactly as chosen — no conversion
        rpe:           rpe,
        // avg_form_score intentionally omitted → backend default 0.0 (no camera data)
        pain_flag:     false,
        pain_location: '',
        duration_seconds: durSec
      };

      const res = await fetch('/set/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || 'Failed to log set ' + i);
      }

      const data = await res.json();
      manualSessionId = data.session_id;   // reuse the same session for subsequent sets
    }

    // Finalize the session so calories + stats are computed
    const endRes = await fetch('/session/end', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: manualSessionId, notes })
    });

    if (!endRes.ok) throw new Error('Failed to finalize session.');

    statusEl.style.display = 'block';
    statusEl.style.background = 'rgba(0,200,83,0.12)';
    statusEl.style.color = '#00c853';
    statusEl.style.border = '1px solid rgba(0,200,83,0.3)';
    statusEl.textContent = `✓ Logged ${setsCount} set${setsCount > 1 ? 's' : ''} of ${document.getElementById('manualExerciseSelect').selectedOptions[0].text}. Check History to verify.`;
    saveBtn.textContent = 'Saved!';

    // Keep modal open briefly so user sees confirmation, then close
    setTimeout(closeManualEntryModal, 2500);

  } catch (e) {
    console.error('saveManualEntry error:', e);
    statusEl.style.display = 'block';
    statusEl.style.background = 'rgba(255,23,68,0.1)';
    statusEl.style.color = '#ff5252';
    statusEl.style.border = '1px solid rgba(255,23,68,0.3)';
    statusEl.textContent = 'Error: ' + e.message;
    saveBtn.disabled = false;
    saveBtn.textContent = 'Save All Sets';
  }
}
