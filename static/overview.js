// FitSense AI — Overview Page Logic

let selectedWeightDays = '7';
let activeCardioTab = 'duration';

document.addEventListener('DOMContentLoaded', async () => {
  injectNav('overview');
  const user = await initAuth();
  if (!user) return;

  await fetchProfile();

  // Check profile completeness for banner
  const p = window.activeProfile;
  const setupBanner = document.getElementById('setupBanner');
  if (setupBanner) {
    const isComplete = p && p.weight_kg && p.height_cm && p.age && p.sex;
    setupBanner.style.display = isComplete ? 'none' : 'flex';
  }

  setupEventListeners();
  await refreshDashboard();
});

function setupEventListeners() {
  // Weight range buttons
  document.querySelectorAll('.btn-range').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      document.querySelectorAll('.btn-range').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      selectedWeightDays = e.target.getAttribute('data-days');
      await fetchWeightHistoryAndDraw();
    });
  });

  // Quick weight modal
  const quickWeightBtn = document.getElementById('quickWeightBtn');
  const weightModal = document.getElementById('weightModal');
  const closeWeightBtn = document.getElementById('closeWeightBtn');
  const saveWeightBtn = document.getElementById('saveWeightBtn');
  quickWeightBtn.addEventListener('click', () => {
    document.getElementById('quickWeightInput').value = window.activeProfile ? window.activeProfile.weight_kg : 75.0;
    document.getElementById('quickWeightDate').value = new Date().toISOString().split('T')[0];
    weightModal.classList.add('active');
  });
  closeWeightBtn.addEventListener('click', () => weightModal.classList.remove('active'));
  saveWeightBtn.addEventListener('click', saveWeight);

  // Food modal
  const logFoodBtn = document.getElementById('logFoodBtn');
  const foodModal = document.getElementById('foodModal');
  const closeFoodBtn = document.getElementById('closeFoodBtn');
  const saveFoodBtn = document.getElementById('saveFoodBtn');
  logFoodBtn.addEventListener('click', () => {
    document.getElementById('foodDate').value = new Date().toISOString().split('T')[0];
    document.getElementById('foodCalories').value = '';
    document.getElementById('foodProtein').value = 0;
    document.getElementById('foodCarbs').value = 0;
    document.getElementById('foodFat').value = 0;
    foodModal.classList.add('active');
  });
  closeFoodBtn.addEventListener('click', () => foodModal.classList.remove('active'));
  saveFoodBtn.addEventListener('click', saveFood);

  // Cardio modal
  const logCardioBtn = document.getElementById('logCardioBtn');
  const cardioModal = document.getElementById('cardioModal');
  const closeCardioBtn = document.getElementById('closeCardioBtn');
  const saveCardioBtn = document.getElementById('saveCardioBtn');
  logCardioBtn.addEventListener('click', () => {
    document.getElementById('cardioDate').value = new Date().toISOString().split('T')[0];
    document.getElementById('cardioDuration').value = 30;
    document.getElementById('cardioOverrideVal').value = '';
    document.getElementById('overrideCalorieCheckbox').checked = false;
    document.getElementById('overrideCalorieGroup').style.display = 'none';
    document.getElementById('cardioActivityName').value = '';
    document.getElementById('cardioDirectCalories').value = '';
    document.getElementById('cardioDirectDuration').value = '';
    document.getElementById('customMetGroup').style.display = 'none';
    updateCardioEstimate();
    cardioModal.classList.add('active');
  });
  closeCardioBtn.addEventListener('click', () => cardioModal.classList.remove('active'));
  saveCardioBtn.addEventListener('click', saveCardio);

  // Cardio tab triggers
  const tabDurationBtn = document.getElementById('tabDurationBtn');
  const tabDirectBtn = document.getElementById('tabDirectBtn');
  const panelDuration = document.getElementById('panelDuration');
  const panelDirect = document.getElementById('panelDirect');
  tabDurationBtn.addEventListener('click', () => {
    activeCardioTab = 'duration';
    tabDurationBtn.classList.add('active');
    tabDirectBtn.classList.remove('active');
    panelDuration.style.display = 'block';
    panelDirect.style.display = 'none';
  });
  tabDirectBtn.addEventListener('click', () => {
    activeCardioTab = 'direct';
    tabDirectBtn.classList.add('active');
    tabDurationBtn.classList.remove('active');
    panelDuration.style.display = 'none';
    panelDirect.style.display = 'block';
  });

  const cardioPresetSelect = document.getElementById('cardioPresetSelect');
  const cardioDuration = document.getElementById('cardioDuration');
  const cardioCustomMet = document.getElementById('cardioCustomMet');
  const overrideCalorieCheckbox = document.getElementById('overrideCalorieCheckbox');
  cardioPresetSelect.addEventListener('change', (e) => {
    document.getElementById('customMetGroup').style.display = e.target.value === 'Other' ? 'flex' : 'none';
    updateCardioEstimate();
  });
  cardioDuration.addEventListener('input', updateCardioEstimate);
  cardioCustomMet.addEventListener('input', updateCardioEstimate);
  overrideCalorieCheckbox.addEventListener('change', (e) => {
    document.getElementById('overrideCalorieGroup').style.display = e.target.checked ? 'flex' : 'none';
  });
}

async function refreshDashboard() {
  try {
    const res = await fetch('/dashboard/today');
    if (!res.ok) return;
    const data = await res.json();
    const nutrition = data.nutrition;

    const netVal = Math.round(nutrition.net_calories);
    const netEl = document.getElementById('netCaloriesDisplay');
    netEl.textContent = `${netVal > 0 ? '+' : ''}${netVal} kcal`;
    netEl.className = netVal < 0 ? 'net-cal-val deficit' : netVal > 0 ? 'net-cal-val surplus' : 'net-cal-val';

    document.getElementById('calsConsumed').textContent = `${Math.round(nutrition.calories_consumed)} kcal`;
    document.getElementById('calsBurned').textContent   = `${Math.round(nutrition.calories_burned_exercise)} kcal`;
    document.getElementById('calsBmr').textContent      = `${Math.round(nutrition.calories_burned_bmr)} kcal`;
    document.getElementById('calsTef').textContent      = `${Math.round(nutrition.tef_calories)} kcal`;

    document.getElementById('macroProtein').textContent = `${Math.round(nutrition.protein_g)}g`;
    document.getElementById('macroCarbs').textContent   = `${Math.round(nutrition.carbs_g)}g`;
    document.getElementById('macroFat').textContent     = `${Math.round(nutrition.fat_g)}g`;

    document.getElementById('currentWeightDisplay').textContent = `${data.current_weight.toFixed(1)} kg`;

    await fetchWeightHistoryAndDraw();
  } catch (e) {
    console.error('refreshDashboard error:', e);
  }
}

async function fetchWeightHistoryAndDraw() {
  try {
    const res = await fetch(`/weight/history?days=${selectedWeightDays}`);
    if (res.ok) drawWeightChart(await res.json());
  } catch (e) {
    console.error('fetchWeightHistoryAndDraw error:', e);
  }
}

function drawWeightChart(data) {
  const canvas = document.getElementById('weightChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const weightChangeDisplay = document.getElementById('weightChangeDisplay');

  if (!data || data.length === 0) {
    ctx.fillStyle = '#aaaaaa';
    ctx.font = '13px Inter';
    ctx.textAlign = 'center';
    ctx.fillText('No weight history data available. Log weight to begin.', canvas.width / 2, canvas.height / 2);
    weightChangeDisplay.textContent = '-- kg';
    return;
  }

  const firstW = data[0].weight_kg;
  const lastW  = data[data.length - 1].weight_kg;
  const delta  = lastW - firstW;
  weightChangeDisplay.textContent = (delta >= 0 ? '+' : '') + delta.toFixed(1) + ' kg';
  weightChangeDisplay.style.color = delta < 0 ? '#29b6f6' : delta > 0 ? '#ffa726' : '#ffffff';

  const pL = 45, pR = 20, pT = 25, pB = 35;
  const gW = canvas.width - pL - pR;
  const gH = canvas.height - pT - pB;

  const weights = data.map(d => d.weight_kg);
  let minW = Math.min(...weights) - 2;
  let maxW = Math.max(...weights) + 2;
  if (maxW - minW < 4) { minW -= 2; maxW += 2; }

  ctx.strokeStyle = '#2c2c2c'; ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(pL, pT);
  ctx.lineTo(pL, canvas.height - pB);
  ctx.lineTo(canvas.width - pR, canvas.height - pB);
  ctx.stroke();

  ctx.fillStyle = '#aaaaaa'; ctx.font = '10px Inter';
  ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
  for (let i = 0; i <= 4; i++) {
    const yVal = minW + (maxW - minW) * (i / 4);
    const yPos = canvas.height - pB - (i / 4) * gH;
    ctx.strokeStyle = '#1f1f1f';
    ctx.beginPath(); ctx.moveTo(pL, yPos); ctx.lineTo(canvas.width - pR, yPos); ctx.stroke();
    ctx.fillText(yVal.toFixed(1), pL - 8, yPos);
  }

  const numPoints = data.length;
  const points = data.map((d, idx) => ({
    x: pL + (numPoints > 1 ? (idx / (numPoints - 1)) * gW : gW / 2),
    y: canvas.height - pB - ((d.weight_kg - minW) / (maxW - minW)) * gH,
    date: d.date,
    weight: d.weight_kg
  }));

  if (points.length > 1) {
    ctx.fillStyle = 'rgba(41, 182, 246, 0.07)';
    ctx.beginPath();
    ctx.moveTo(points[0].x, canvas.height - pB);
    points.forEach(p => ctx.lineTo(p.x, p.y));
    ctx.lineTo(points[points.length - 1].x, canvas.height - pB);
    ctx.closePath(); ctx.fill();
  }

  ctx.strokeStyle = '#29b6f6'; ctx.lineWidth = 3;
  ctx.beginPath();
  points.forEach((p, i) => { if (i === 0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y); });
  ctx.stroke();

  const MAX_LABELS = 5;
  const labelIdx = new Set([0, numPoints - 1]);
  if (numPoints <= MAX_LABELS) {
    for (let i = 0; i < numPoints; i++) labelIdx.add(i);
  } else {
    const interior = MAX_LABELS - 2;
    for (let k = 1; k <= interior; k++) labelIdx.add(Math.round(k * (numPoints - 1) / (interior + 1)));
  }

  points.forEach((p, idx) => {
    ctx.fillStyle = '#ffffff';
    ctx.beginPath(); ctx.arc(p.x, p.y, 4, 0, 2 * Math.PI); ctx.fill();
    ctx.strokeStyle = '#29b6f6'; ctx.lineWidth = 1.5; ctx.stroke();
    if (labelIdx.has(idx)) {
      ctx.fillStyle = '#aaaaaa'; ctx.font = '9px Inter'; ctx.textAlign = 'center';
      const parts = p.date ? p.date.split('-') : [];
      ctx.fillText(parts.length === 3 ? `${parts[1]}/${parts[2]}` : (p.date || ''), p.x, canvas.height - pB + 15);
      ctx.fillStyle = '#ffffff';
      ctx.fillText(p.weight.toFixed(1), p.x, p.y - 10);
    }
  });
}

async function saveWeight() {
  const payload = {
    weight_kg: parseFloat(document.getElementById('quickWeightInput').value) || 0.0,
    date: document.getElementById('quickWeightDate').value
  };
  try {
    const res = await fetch('/weight/log', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    if (res.ok) {
      document.getElementById('weightModal').classList.remove('active');
      await fetchProfile();
      await refreshDashboard();
    }
  } catch (e) { console.error('saveWeight error:', e); }
}

async function saveFood() {
  const payload = {
    date: document.getElementById('foodDate').value,
    calories_consumed: parseFloat(document.getElementById('foodCalories').value) || 0.0,
    protein_g: parseFloat(document.getElementById('foodProtein').value) || 0.0,
    carbs_g: parseFloat(document.getElementById('foodCarbs').value) || 0.0,
    fat_g: parseFloat(document.getElementById('foodFat').value) || 0.0,
  };
  try {
    const res = await fetch('/nutrition/log', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    if (res.ok) {
      document.getElementById('foodModal').classList.remove('active');
      await refreshDashboard();
    }
  } catch (e) { console.error('saveFood error:', e); }
}

function updateCardioEstimate() {
  const metValues = { Running: 9.8, Cycling: 7.5, Swimming: 7.0, Walking: 3.5, Sports: 8.0, Other: 0.0 };
  const preset = document.getElementById('cardioPresetSelect').value;
  let met = metValues[preset];
  if (preset === 'Other') met = parseFloat(document.getElementById('cardioCustomMet').value) || 5.0;
  const mins = parseFloat(document.getElementById('cardioDuration').value) || 0;
  const userWeight = window.activeProfile ? window.activeProfile.weight_kg : 75.0;
  const cals = met * userWeight * (mins / 60.0);
  document.getElementById('cardioEstimatedDisplay').textContent = `${Math.round(cals)} kcal`;
  if (!document.getElementById('overrideCalorieCheckbox').checked)
    document.getElementById('cardioOverrideVal').value = Math.round(cals);
}

async function saveCardio() {
  let activity, duration, calories, method;
  if (activeCardioTab === 'duration') {
    activity = document.getElementById('cardioPresetSelect').value;
    duration = parseFloat(document.getElementById('cardioDuration').value) || 0.0;
    calories = parseFloat(document.getElementById('cardioOverrideVal').value) || 0.0;
    method   = 'duration';
  } else {
    activity = document.getElementById('cardioActivityName').value || 'Cardio Workout';
    duration = parseFloat(document.getElementById('cardioDirectDuration').value) || 0.0;
    calories = parseFloat(document.getElementById('cardioDirectCalories').value) || 0.0;
    method   = 'direct_calories';
  }
  const payload = { date: document.getElementById('cardioDate').value, activity_name: activity, duration_mins: duration, calories_burned: calories, entry_method: method };
  try {
    const res = await fetch('/cardio/log', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    if (res.ok) {
      document.getElementById('cardioModal').classList.remove('active');
      await refreshDashboard();
    }
  } catch (e) { console.error('saveCardio error:', e); }
}
