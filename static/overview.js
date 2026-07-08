// FitSense AI — Overview Page Logic

let selectedWeightDays = '7';
let activeCardioTab = 'duration';
let userGoalType = null;
let userTargetWeight = null;
let userStartingWeight = null;
let userTargetDate = null;
let currentWeightVal = 75.0;
let userProfile = null;

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
  await fetchFitnessScore();
  await initStrengthAnalytics();
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
    
    // Reset search fields
    document.getElementById('foodSearchInput').value = '';
    document.getElementById('foodSearchResults').style.display = 'none';
    document.getElementById('selectedFoodContainer').style.display = 'none';
    window.selectedFood = null;

    // Reset meal category filters
    const categoryInput = document.getElementById('selectedMealCategory');
    if (categoryInput) categoryInput.value = 'any';
    document.querySelectorAll('.meal-category-pill').forEach(p => p.classList.remove('active'));
    
    foodModal.classList.add('active');
  });
  closeFoodBtn.addEventListener('click', () => {
    if (window.closeBarcodeScanner) {
      window.closeBarcodeScanner();
    }
    foodModal.classList.remove('active');
  });
  saveFoodBtn.addEventListener('click', saveFood);

  // Setup Food Search listeners
  let foodSearchDebounceTimer = null;
  const foodSearchInput = document.getElementById('foodSearchInput');
  const foodSearchResults = document.getElementById('foodSearchResults');
  const foodQuantityInput = document.getElementById('foodQuantity');
  const clearSelectedFoodBtn = document.getElementById('clearSelectedFoodBtn');

  async function performFoodSearch() {
    if (!foodSearchInput || !foodSearchResults) return;
    const q = foodSearchInput.value.trim();
    const cat = document.getElementById('selectedMealCategory').value;

    if (q.length < 2 && cat === 'any') {
      foodSearchResults.style.display = 'none';
      return;
    }

    try {
      const res = await fetch(`/food/search?q=${encodeURIComponent(q)}&category=${encodeURIComponent(cat)}`);
      if (res.ok) {
        const foods = await res.json();
        renderFoodSearchResults(foods);
      }
    } catch (e) {
      console.error('Error searching food:', e);
    }
  }

  function toggleMealCategoryFilter(value) {
    const pills = document.querySelectorAll('.meal-category-pill');
    const input = document.getElementById('selectedMealCategory');
    if (!input) return;

    const currentVal = input.value;
    if (currentVal === value) {
      input.value = 'any';
      pills.forEach(p => p.classList.remove('active'));
    } else {
      input.value = value;
      pills.forEach(p => {
        if (p.getAttribute('data-value') === value) {
          p.classList.add('active');
        } else {
          p.classList.remove('active');
        }
      });
    }

    performFoodSearch();
  }
  window.toggleMealCategoryFilter = toggleMealCategoryFilter;

  if (foodSearchInput) {
    foodSearchInput.addEventListener('input', () => {
      clearTimeout(foodSearchDebounceTimer);
      foodSearchDebounceTimer = setTimeout(performFoodSearch, 300);
    });
  }

  function renderFoodSearchResults(foods) {
    foodSearchResults.innerHTML = '';
    if (!foods || foods.length === 0) {
      const emptyDiv = document.createElement('div');
      emptyDiv.className = 'search-result-item';
      emptyDiv.style.cursor = 'default';
      emptyDiv.textContent = 'No foods found';
      foodSearchResults.appendChild(emptyDiv);
      foodSearchResults.style.display = 'block';
      return;
    }
    foods.forEach(food => {
      const item = document.createElement('div');
      item.className = 'search-result-item';
      item.innerHTML = `<strong>${food.name}</strong> <span style="font-size:0.82rem; color:#a6adc8;">(${food.calories} kcal, P: ${food.protein_g}g, C: ${food.carbs_g}g, F: ${food.fat_g}g)</span>`;
      item.addEventListener('click', () => {
        selectFood(food);
      });
      foodSearchResults.appendChild(item);
    });
    foodSearchResults.style.display = 'block';
  }

  function selectFood(food) {
    window.selectedFood = food;
    document.getElementById('selectedFoodName').textContent = `Selected: ${food.name}`;
    document.getElementById('foodQuantity').value = '1.0';
    document.getElementById('selectedFoodContainer').style.display = 'block';
    foodSearchResults.style.display = 'none';
    foodSearchInput.value = '';
    updateCalculatedNutrients();
  }

  function updateCalculatedNutrients() {
    if (!window.selectedFood) return;
    const qty = parseFloat(document.getElementById('foodQuantity').value) || 1.0;
    document.getElementById('foodCalories').value = Math.round(window.selectedFood.calories * qty);
    document.getElementById('foodProtein').value = (window.selectedFood.protein_g * qty).toFixed(1);
    document.getElementById('foodCarbs').value = (window.selectedFood.carbs_g * qty).toFixed(1);
    document.getElementById('foodFat').value = (window.selectedFood.fat_g * qty).toFixed(1);
  }

  if (foodQuantityInput) {
    foodQuantityInput.addEventListener('input', updateCalculatedNutrients);
  }

  if (clearSelectedFoodBtn) {
    clearSelectedFoodBtn.addEventListener('click', () => {
      window.selectedFood = null;
      document.getElementById('selectedFoodContainer').style.display = 'none';
      document.getElementById('foodCalories').value = '';
      document.getElementById('foodProtein').value = 0;
      document.getElementById('foodCarbs').value = 0;
      document.getElementById('foodFat').value = 0;
    });
  }

  document.addEventListener('click', (e) => {
    if (foodSearchResults && !foodSearchInput.contains(e.target) && !foodSearchResults.contains(e.target)) {
      foodSearchResults.style.display = 'none';
    }
  });

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

  // AI Coach Tip button
  const getCoachTipBtn = document.getElementById('getCoachTipBtn');
  if (getCoachTipBtn) {
    getCoachTipBtn.addEventListener('click', fetchCoachTip);
  }

  // AI Insights button
  const getInsightsBtn = document.getElementById('getInsightsBtn');
  if (getInsightsBtn) {
    getInsightsBtn.addEventListener('click', fetchInsights);
  }

  // Barcode scanner implementation
  let barcodeStream = null;

  function openBarcodeScanner() {
    const section = document.getElementById('barcodeScannerSection');
    const video = document.getElementById('barcodeVideo');
    const status = document.getElementById('barcodeScanStatus');
    
    if (!section || !video) return;

    status.textContent = "Requesting camera access...";
    status.style.color = "#a6adc8";
    section.style.display = 'flex';

    navigator.mediaDevices.getUserMedia({ 
      video: { 
        width: { ideal: 640 }, 
        height: { ideal: 480 },
        facingMode: "environment"
      } 
    }).then(stream => {
      barcodeStream = stream;
      video.srcObject = stream;
      video.play();
      status.textContent = "Camera active. Hold a barcode steady in the target box.";
    }).catch(error => {
      console.error("Camera access error:", error);
      status.textContent = "Camera access error. Please grant permissions and retry.";
      status.style.color = "#f38ba8";
    });
  }
  window.openBarcodeScanner = openBarcodeScanner;

  function closeBarcodeScanner() {
    const section = document.getElementById('barcodeScannerSection');
    const video = document.getElementById('barcodeVideo');
    const status = document.getElementById('barcodeScanStatus');

    if (barcodeStream) {
      barcodeStream.getTracks().forEach(track => track.stop());
      barcodeStream = null;
    }

    if (video) {
      video.srcObject = null;
    }

    if (section) {
      section.style.display = 'none';
    }
    
    if (status) {
      status.textContent = "";
    }
  }
  window.closeBarcodeScanner = closeBarcodeScanner;

  async function captureAndScanBarcode() {
    const video = document.getElementById('barcodeVideo');
    const canvas = document.getElementById('barcodeCanvas');
    const status = document.getElementById('barcodeScanStatus');

    if (!video || !canvas || !status || !barcodeStream) return;

    status.textContent = "Scanning frame...";
    status.style.color = "#89b4fa";

    try {
      const ctx = canvas.getContext('2d');
      canvas.width = video.videoWidth || 640;
      canvas.height = video.videoHeight || 480;
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      
      const dataUrl = canvas.toDataURL('image/jpeg', 0.85);

      const res = await fetch('/food/scan-barcode', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image_base64: dataUrl })
      });

      if (res.ok) {
        const food = await res.json();
        status.textContent = "Product recognized!";
        status.style.color = "#a6e3a1";
        
        selectFood(food);
        
        setTimeout(() => {
          closeBarcodeScanner();
        }, 500);
      } else {
        const err = await res.json();
        status.textContent = err.detail || "Barcode not recognized. Align and try again.";
        status.style.color = "#f38ba8";
      }
    } catch (error) {
      console.error("Scan API error:", error);
      status.textContent = "Network or lookup error. Please try again.";
      status.style.color = "#f38ba8";
    }
  }
  window.captureAndScanBarcode = captureAndScanBarcode;
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
    currentWeightVal = data.current_weight ? parseFloat(data.current_weight) : 75.0;

    // Calculate and display BMI
    const bmiValEl = document.getElementById('bmiDisplay');
    const bmiStatusEl = document.getElementById('bmiStatusDisplay');
    if (bmiValEl && bmiStatusEl) {
      const heightCm = data.profile ? parseFloat(data.profile.height_cm) : 0;
      const weightKg = data.current_weight ? parseFloat(data.current_weight) : 0;
      if (heightCm > 0 && weightKg > 0) {
        const bmi = weightKg / ((heightCm / 100.0) ** 2);
        bmiValEl.textContent = bmi.toFixed(1);
        
        let status = 'Normal';
        let statusColor = '#a6e3a1'; // Catppuccin Green
        if (bmi < 18.5) {
          status = 'Underweight';
          statusColor = '#b4befe'; // Catppuccin Lavender
        } else if (bmi >= 25 && bmi < 30) {
          status = 'Overweight';
          statusColor = '#fab387'; // Catppuccin Peach
        } else if (bmi >= 30) {
          status = 'Obese';
          statusColor = '#f38ba8'; // Catppuccin Red/Pink
        }
        bmiStatusEl.textContent = status;
        bmiStatusEl.style.color = statusColor;
      } else {
        bmiValEl.textContent = '--';
        bmiStatusEl.textContent = '--';
        bmiStatusEl.style.color = 'inherit';
      }
    }

    // Calculate and display calorie target and progress
    const calorieTarget = calculateTargetCalories(data.profile);
    const consumedVal = nutrition.calories_consumed || 0.0;
    const targetEl = document.getElementById('calsTarget');
    const progressBar = document.getElementById('calorieProgressBar');
    const progressPctText = document.getElementById('calorieProgressPct');
    const progressStatus = document.getElementById('calorieProgressStatus');

    if (calorieTarget === null) {
      if (targetEl) {
        targetEl.textContent = 'Setup Profile';
        targetEl.style.fontSize = '0.75rem';
        targetEl.style.color = '#f38ba8';
      }
      if (progressBar && progressPctText && progressStatus) {
        progressBar.style.width = `0%`;
        progressPctText.textContent = `0%`;
        progressStatus.innerHTML = '<span style="color:#f38ba8; font-weight:600;">Please <a href="/profile-page" style="color:#f38ba8; text-decoration:underline;">complete your profile</a> first.</span>';
      }
    } else {
      if (targetEl) {
        targetEl.textContent = `${calorieTarget} kcal`;
        targetEl.style.fontSize = '';
        targetEl.style.color = '';
      }
      
      const progressPct = Math.min(100, Math.round((consumedVal / calorieTarget) * 100));
      if (progressBar && progressPctText && progressStatus) {
        progressBar.style.width = `${progressPct}%`;
        progressPctText.textContent = `${progressPct}%`;
        
        const diff = calorieTarget - consumedVal;
        if (diff >= 0) {
          progressBar.style.backgroundColor = 'var(--color-blue)';
          progressStatus.textContent = `${Math.round(diff)} kcal under target`;
          progressStatus.style.color = 'var(--color-blue)';
        } else {
          progressBar.style.backgroundColor = 'var(--color-orange)';
          progressStatus.textContent = `${Math.round(Math.abs(diff))} kcal over target`;
          progressStatus.style.color = 'var(--color-orange)';
        }
      }
    }

    // Set global goal values
    userProfile = data.profile;
    userGoalType = data.profile ? data.profile.goal_type : null;
    userTargetWeight = data.profile && data.profile.target_weight_kg ? parseFloat(data.profile.target_weight_kg) : null;
    userStartingWeight = data.profile && data.profile.starting_weight_kg ? parseFloat(data.profile.starting_weight_kg) : null;
    userTargetDate = data.profile ? data.profile.target_date : null;

    // Render Weight Goal section
    const noGoalState = document.getElementById('noGoalState');
    const activeGoalState = document.getElementById('activeGoalState');
    
    if (noGoalState && activeGoalState) {
      if (!userGoalType) {
        noGoalState.style.display = 'block';
        activeGoalState.style.display = 'none';
      } else {
        noGoalState.style.display = 'none';
        activeGoalState.style.display = 'flex';
        
        // Update texts
        const badge = document.getElementById('goalTypeBadge');
        if (userGoalType === 'lose') {
          badge.textContent = 'Weight Loss Goal';
          badge.style.background = 'rgba(243, 139, 168, 0.15)';
          badge.style.color = '#f38ba8';
          badge.style.borderColor = 'rgba(243, 139, 168, 0.3)';
        } else if (userGoalType === 'gain') {
          badge.textContent = 'Weight Gain Goal';
          badge.style.background = 'rgba(166, 227, 161, 0.15)';
          badge.style.color = '#a6e3a1';
          badge.style.borderColor = 'rgba(166, 227, 161, 0.3)';
        } else {
          badge.textContent = 'Maintenance Goal';
          badge.style.background = 'rgba(180, 190, 254, 0.15)';
          badge.style.color = '#b4befe';
          badge.style.borderColor = 'rgba(180, 190, 254, 0.3)';
        }
        
        const currentW = data.current_weight || userStartingWeight || 0.0;
        document.getElementById('goalTargetText').textContent = `Target: ${userTargetWeight.toFixed(1)} kg`;
        document.getElementById('goalStartWeightText').textContent = `Start: ${userStartingWeight.toFixed(1)} kg`;
        document.getElementById('goalTargetWeightText').textContent = `Target: ${userTargetWeight.toFixed(1)} kg`;
        
        // Remaining
        const remaining = Math.abs(currentW - userTargetWeight);
        const remainingEl = document.getElementById('goalRemainingText');
        if (remaining <= 0.1 && userGoalType === 'maintain') {
          remainingEl.textContent = 'On track';
        } else {
          remainingEl.textContent = `${remaining.toFixed(1)} kg to go`;
        }

        // Show pace and timeline details clearly on the goal card
        const paceEl = document.getElementById('goalPaceText');
        const statusEl = document.getElementById('goalScheduleStatus');

        if (userGoalType === 'maintain') {
          const focusStr = (data.profile.maintenance_focus === 'build_muscle') ? 'Build Muscle (Recomp)' : 'Stay Fit';
          if (paceEl) paceEl.textContent = `Focus: ${focusStr}`;
          if (statusEl) {
            statusEl.textContent = `Target Band: ${(userTargetWeight - 1.5).toFixed(1)} - ${(userTargetWeight + 1.5).toFixed(1)} kg`;
            statusEl.style.color = '#b4befe';
          }
        } else {
          const paceVal = data.profile.pace || 'normal';
          let pacePct = 0.005;
          if (paceVal === 'mild') pacePct = 0.0025;
          else if (paceVal === 'aggressive') pacePct = 0.01;

          const baseWeight = userStartingWeight || currentW;
          const weeklyRate = baseWeight * pacePct;
          const estimatedWeeks = weeklyRate > 0 ? remaining / weeklyRate : 0;
          const musclePreserve = data.profile.muscle_focus === 'preserve' ? ' [muscle preservation]' : '';

          if (paceEl) {
            paceEl.textContent = `Rate: ${weeklyRate.toFixed(2)} kg/wk (${paceVal}${musclePreserve})`;
          }
          if (statusEl) {
            if (userTargetDate) {
              const tDate = new Date(userTargetDate);
              statusEl.textContent = `Est. Target Date: ${tDate.toLocaleDateString(undefined, {month: 'short', day: 'numeric', year: 'numeric'})} (~${Math.ceil(estimatedWeeks)} wk remaining)`;
            } else {
              statusEl.textContent = `Estimated Duration: ~${Math.ceil(estimatedWeeks)} weeks`;
            }
            statusEl.style.color = userGoalType === 'lose' ? '#f38ba8' : '#a6e3a1';
          }
        }
        
        // Progress percentage calculation
        let progressPct = 0;
        if (userGoalType === 'lose') {
          if (userStartingWeight > userTargetWeight) {
            progressPct = Math.round(((userStartingWeight - currentW) / (userStartingWeight - userTargetWeight)) * 100);
          }
        } else if (userGoalType === 'gain') {
          if (userTargetWeight > userStartingWeight) {
            progressPct = Math.round(((currentW - userStartingWeight) / (userTargetWeight - userStartingWeight)) * 100);
          }
        } else {
          // Maintenance is 100% progress if within ±1.5kg
          progressPct = remaining <= 1.5 ? 100 : Math.round((1.5 / remaining) * 100);
        }
        progressPct = Math.max(0, Math.min(100, progressPct));
        
        document.getElementById('goalProgressPct').textContent = `${progressPct}%`;
        document.getElementById('goalProgressBar').style.width = `${progressPct}%`;
      }
    }

    // Fetch and render nutrition alerts
    try {
      const alertsRes = await fetch('/nutrition/alerts');
      if (alertsRes.ok) {
        const alerts = await alertsRes.json();
        const container = document.getElementById('nutritionAlertsContainer');
        if (container) {
          container.innerHTML = '';
          if (alerts && alerts.length > 0) {
            alerts.forEach(alert => {
              const div = document.createElement('div');
              div.className = `nutrition-alert nutrition-alert-${alert.type}`;
              const iconSvg = `<svg style="width: 18px; height: 18px; flex-shrink: 0;" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>`;
              div.innerHTML = `${iconSvg}<span>${alert.message}</span>`;
              container.appendChild(div);
            });
            container.style.display = 'flex';
          } else {
            const div = document.createElement('div');
            div.className = 'nutrition-alert nutrition-alert-success';
            const iconSvg = `<svg style="width: 18px; height: 18px; flex-shrink: 0;" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>`;
            div.innerHTML = `${iconSvg}<span>All nutrition targets on track today!</span>`;
            container.appendChild(div);
            container.style.display = 'flex';
          }
        }
      }
    } catch (alertsErr) {
      console.error('Error fetching alerts:', alertsErr);
    }

    await fetchWeightHistoryAndDraw();
    await fetchNutritionHistoryAndDraw();
    await checkWeeklyWeighIn(data.profile, data.current_weight);
    await fetchFormInsights();
  } catch (e) {
    console.error('refreshDashboard error:', e);
  }
}

async function fetchWeightHistoryAndDraw() {
  try {
    const res = await fetch(`/weight/history?days=${selectedWeightDays}`);
    if (res.ok) {
      const data = await res.json();
      drawWeightChart(data, userTargetWeight, userGoalType);
    }
  } catch (e) {
    console.error('fetchWeightHistoryAndDraw error:', e);
  }
}

function drawWeightChart(data, targetWeight = null, goalType = null) {
  const canvas = document.getElementById('weightChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const weightChangeDisplay = document.getElementById('weightChangeDisplay');

  // Handle pace & schedule DOM elements
  const goalPaceText = document.getElementById('goalPaceText');
  const goalScheduleStatus = document.getElementById('goalScheduleStatus');

  if (!data || data.length === 0) {
    ctx.fillStyle = '#aaaaaa';
    ctx.font = '13px Inter';
    ctx.textAlign = 'center';
    ctx.fillText('No weight entries logged yet. Log your weight to see your progress chart.', canvas.width / 2, canvas.height / 2);
    weightChangeDisplay.textContent = '-- kg';
    if (goalPaceText) goalPaceText.textContent = "Pace: Not enough data yet";
    if (goalScheduleStatus) goalScheduleStatus.textContent = "";
    return;
  }

  const firstW = data[0].weight_kg;
  const lastW  = data[data.length - 1].weight_kg;
  const delta  = lastW - firstW;
  weightChangeDisplay.textContent = (delta >= 0 ? '+' : '') + delta.toFixed(1) + ' kg';
  weightChangeDisplay.style.color = delta < 0 ? '#29b6f6' : delta > 0 ? '#ffa726' : '#ffffff';

  // Pace & schedule calculation
  if (goalPaceText && goalScheduleStatus) {
    if (data.length >= 2) {
      const daysDiff = (new Date(data[data.length - 1].date) - new Date(data[0].date)) / (1000 * 60 * 60 * 24);
      if (daysDiff >= 3) {
        const weightDiff = lastW - firstW;
        const pacePerWeek = (weightDiff / daysDiff) * 7;
        goalPaceText.textContent = `Pace: ${(pacePerWeek >= 0 ? '+' : '') + pacePerWeek.toFixed(2)} kg/week`;

        if (userTargetDate && targetWeight && goalType) {
          const daysRemaining = (new Date(userTargetDate) - new Date()) / (1000 * 60 * 60 * 24);
          if (daysRemaining > 0) {
            const weightRemaining = targetWeight - lastW;
            const requiredPace = (weightRemaining / daysRemaining) * 7;
            let schedule = "On track";
            let color = "#a6e3a1";

            if (goalType === 'lose') {
              if (pacePerWeek > requiredPace + 0.1) {
                schedule = "Behind schedule";
                color = "#fab387";
              } else if (pacePerWeek < requiredPace - 0.1) {
                schedule = "Ahead of schedule";
                color = "#a6e3a1";
              }
            } else if (goalType === 'gain') {
              if (pacePerWeek < requiredPace - 0.1) {
                schedule = "Behind schedule";
                color = "#fab387";
              } else if (pacePerWeek > requiredPace + 0.1) {
                schedule = "Ahead of schedule";
                color = "#a6e3a1";
              }
            }
            goalScheduleStatus.textContent = schedule;
            goalScheduleStatus.style.color = color;
          } else {
            goalScheduleStatus.textContent = "Goal target date passed";
            goalScheduleStatus.style.color = "#f38ba8";
          }
        } else {
          goalScheduleStatus.textContent = "";
        }
      } else {
        goalPaceText.textContent = "Pace: Not enough data yet";
        goalScheduleStatus.textContent = "";
      }
    } else {
      goalPaceText.textContent = "Pace: Not enough data yet";
      goalScheduleStatus.textContent = "";
    }
  }

  const pL = 45, pR = 20, pT = 25, pB = 35;
  const gW = canvas.width - pL - pR;
  const gH = canvas.height - pT - pB;

  const weights = data.map(d => d.weight_kg);
  if (targetWeight && goalType) {
    weights.push(targetWeight);
    if (goalType === 'maintain') {
      weights.push(targetWeight - 1.5);
      weights.push(targetWeight + 1.5);
    }
  }
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

  // Target overlay / Shading / Maintenance Band
  if (targetWeight && goalType) {
    const yTarget = canvas.height - pB - ((targetWeight - minW) / (maxW - minW)) * gH;
    
    if (goalType === 'maintain') {
      const yLower = canvas.height - pB - (((targetWeight - 1.5) - minW) / (maxW - minW)) * gH;
      const yUpper = canvas.height - pB - (((targetWeight + 1.5) - minW) / (maxW - minW)) * gH;

      // Draw maintenance zone shading band
      ctx.fillStyle = 'rgba(166, 227, 161, 0.05)';
      ctx.fillRect(pL, yUpper, gW, yLower - yUpper);

      // Draw dashed limits
      ctx.strokeStyle = 'rgba(166, 227, 161, 0.25)';
      ctx.lineWidth = 1;
      ctx.setLineDash([4, 4]);
      ctx.beginPath(); ctx.moveTo(pL, yUpper); ctx.lineTo(canvas.width - pR, yUpper); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(pL, yLower); ctx.lineTo(canvas.width - pR, yLower); ctx.stroke();
      ctx.setLineDash([]);
      
      // Draw target weight line inside zone
      ctx.strokeStyle = 'rgba(166, 227, 161, 0.4)';
      ctx.lineWidth = 1.5;
      ctx.setLineDash([5, 5]);
      ctx.beginPath(); ctx.moveTo(pL, yTarget); ctx.lineTo(canvas.width - pR, yTarget); ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = '#a6e3a1';
      ctx.font = '9px Inter';
      ctx.textAlign = 'left';
      ctx.fillText(`Target: ${targetWeight.toFixed(1)}kg`, pL + 5, yTarget - 4);
    } else {
      // Lose or gain: shade space between line and target
      if (points.length > 1) {
        ctx.fillStyle = goalType === 'lose' ? 'rgba(243, 139, 168, 0.04)' : 'rgba(166, 227, 161, 0.04)';
        ctx.beginPath();
        ctx.moveTo(points[0].x, points[0].y);
        points.forEach(p => ctx.lineTo(p.x, p.y));
        ctx.lineTo(points[points.length - 1].x, yTarget);
        ctx.lineTo(points[0].x, yTarget);
        ctx.closePath();
        ctx.fill();
      }

      // Draw target weight line
      ctx.strokeStyle = 'rgba(249, 226, 175, 0.4)';
      ctx.lineWidth = 1.5;
      ctx.setLineDash([5, 5]);
      ctx.beginPath(); ctx.moveTo(pL, yTarget); ctx.lineTo(canvas.width - pR, yTarget); ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = '#f9e2af';
      ctx.font = '9px Inter';
      ctx.textAlign = 'left';
      ctx.fillText(`Target: ${targetWeight.toFixed(1)}kg`, pL + 5, yTarget - 4);
    }
  }

  // Draw background area below trend line
  if (points.length > 1) {
    ctx.fillStyle = 'rgba(41, 182, 246, 0.05)';
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
      await fetchFitnessScore();
    }
  } catch (e) { console.error('saveWeight error:', e); }
}

async function saveFood() {
  const dateVal = document.getElementById('foodDate').value;
  let payload = {
    date: dateVal,
    calories_consumed: parseFloat(document.getElementById('foodCalories').value) || 0.0,
    protein_g: parseFloat(document.getElementById('foodProtein').value) || 0.0,
    carbs_g: parseFloat(document.getElementById('foodCarbs').value) || 0.0,
    fat_g: parseFloat(document.getElementById('foodFat').value) || 0.0,
    saturated_fat_g: 0.0,
    fiber_g: 0.0,
    sodium_mg: 0.0,
    sugar_g: 0.0,
    calcium_mg: 0.0,
    iron_mg: 0.0,
    vitamin_c_mg: 0.0
  };

  if (window.selectedFood) {
    const qty = parseFloat(document.getElementById('foodQuantity').value) || 1.0;
    payload.saturated_fat_g = (window.selectedFood.saturated_fat_g || 0.0) * qty;
    payload.fiber_g = (window.selectedFood.fiber_g || 0.0) * qty;
    payload.sodium_mg = (window.selectedFood.sodium_mg || 0.0) * qty;
    payload.sugar_g = (window.selectedFood.sugar_g || 0.0) * qty;
    payload.calcium_mg = (window.selectedFood.calcium_mg || 0.0) * qty;
    payload.iron_mg = (window.selectedFood.iron_mg || 0.0) * qty;
    payload.vitamin_c_mg = (window.selectedFood.vitamin_c_mg || 0.0) * qty;
  }

  try {
    const res = await fetch('/nutrition/log', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    if (res.ok) {
      if (window.closeBarcodeScanner) {
        window.closeBarcodeScanner();
      }
      document.getElementById('foodModal').classList.remove('active');
      await refreshDashboard();
      await fetchFitnessScore();
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
      await fetchFitnessScore();
    }
  } catch (e) { console.error('saveCardio error:', e); }
}

async function fetchCoachTip() {
  const getCoachTipBtn = document.getElementById('getCoachTipBtn');
  const loadingEl = document.getElementById('coachTipLoading');
  const contentEl = document.getElementById('coachTipContent');

  if (!getCoachTipBtn || !loadingEl || !contentEl) return;

  // Show loading state, hide content, disable button
  loadingEl.style.display = 'flex';
  contentEl.style.display = 'none';
  getCoachTipBtn.disabled = true;

  try {
    const res = await fetch('/ai/coach-tip');
    if (!res.ok) {
      throw new Error(`Server returned status ${res.status}`);
    }
    const data = await res.json();
    
    contentEl.innerHTML = '';
    const pEl = document.createElement('p');
    pEl.textContent = data.tip || 'Coach tip unavailable right now';
    contentEl.appendChild(pEl);
  } catch (e) {
    console.error('fetchCoachTip error:', e);
    contentEl.innerHTML = '';
    const pEl = document.createElement('p');
    pEl.className = 'coach-placeholder-text';
    pEl.style.color = 'var(--color-red)';
    pEl.textContent = 'Coach tip unavailable right now';
    contentEl.appendChild(pEl);
  } finally {
    // Hide loading state, show content, enable button
    loadingEl.style.display = 'none';
    contentEl.style.display = 'block';
    getCoachTipBtn.disabled = false;
  }
}

async function fetchFitnessScore() {
  const scoreValEl = document.getElementById('fitnessScoreVal');
  const gradeValEl = document.getElementById('fitnessGradeVal');
  const interpretationEl = document.getElementById('fitnessInterpretation');
  
  if (!scoreValEl || !gradeValEl || !interpretationEl) return;
  
  try {
    const res = await fetch('/fitness-score');
    if (!res.ok) {
      throw new Error(`Failed to fetch fitness score: ${res.status}`);
    }
    const data = await res.json();
    
    scoreValEl.textContent = data.score.toFixed(2);
    gradeValEl.textContent = data.grade;
    
    let text = '';
    const missing = data.missing_inputs || [];
    const lifestyle = data.breakdown.lifestyle;
    const activity = data.breakdown.activity;
    
    if (activity.score === null) {
      text = `Lifestyle score: ${lifestyle.score.toFixed(1)}/10. Log some workouts in the app to factor in activity metrics!`;
    } else {
      text = `Lifestyle sub-score: ${lifestyle.score.toFixed(1)}/10 | Activity sub-score: ${activity.score.toFixed(1)}/10.`;
    }
    
    if (missing.length > 0) {
      const friendlyMissing = missing.map(m => m === 'sleep_hours' ? 'Average Sleep' : m === 'stress_level' ? 'Stress Level' : m);
      text += ` Complete profile inputs for standard tracking: ${friendlyMissing.join(', ')}.`;
    }
    
    interpretationEl.textContent = text;
  } catch (e) {
    console.error('fetchFitnessScore error:', e);
    scoreValEl.textContent = '--';
    gradeValEl.textContent = '--';
    interpretationEl.textContent = 'Fitness score unavailable right now.';
  }
}

async function fetchInsights() {
  const getInsightsBtn = document.getElementById('getInsightsBtn');
  const loadingEl = document.getElementById('insightsLoading');
  const placeholderEl = document.getElementById('insightsPlaceholder');
  const contentEl = document.getElementById('insightsContent');

  if (!getInsightsBtn || !loadingEl || !placeholderEl || !contentEl) return;

  // Show loading state, hide other blocks, disable button
  loadingEl.style.display = 'flex';
  placeholderEl.style.display = 'none';
  contentEl.style.display = 'none';
  getInsightsBtn.disabled = true;

  try {
    const res = await fetch('/ai/insights');
    if (!res.ok) {
      throw new Error(`Server returned status ${res.status}`);
    }
    const data = await res.json();
    
    if (data.error) {
      // Show error clearly
      placeholderEl.innerHTML = `<p class="coach-placeholder-text" style="color: var(--color-red);">${data.error}</p>`;
      placeholderEl.style.display = 'block';
    } else if (data.message) {
      // Empty state / friendly message
      placeholderEl.innerHTML = `<p class="coach-placeholder-text" style="color: var(--color-blue); margin-bottom: 15px;">${data.message}</p>
        <div class="calorie-details-grid" style="grid-template-columns: 1fr 1fr; gap: 12px; width: 100%;">
          <div class="cal-detail-card consumed-card"><span class="lbl">Progress Summary</span><span class="val" style="font-size: 13px; font-weight: 400; line-height: 1.4; margin-top: 6px;">${data.progress_summary}</span></div>
          <div class="cal-detail-card burned-card"><span class="lbl">Tips to Improve</span><span class="val" style="font-size: 13px; font-weight: 400; line-height: 1.4; margin-top: 6px;">${data.tips_to_improve}</span></div>
          <div class="cal-detail-card bmr-card"><span class="lbl">What to Avoid</span><span class="val" style="font-size: 13px; font-weight: 400; line-height: 1.4; margin-top: 6px;">${data.what_to_avoid}</span></div>
          <div class="cal-detail-card tef-card"><span class="lbl">Next Steps</span><span class="val" style="font-size: 13px; font-weight: 400; line-height: 1.4; margin-top: 6px;">${data.next_steps}</span></div>
          <div class="cal-detail-card" style="grid-column: span 2; border-color: rgba(255, 255, 255, 0.15);"><span class="lbl">Motivation Note</span><span class="val" style="font-size: 13px; font-weight: 400; line-height: 1.4; margin-top: 6px;">${data.motivation_note}</span></div>
        </div>`;
      placeholderEl.style.display = 'block';
    } else {
      // Build cards for valid insights
      contentEl.innerHTML = '';
      
      const sections = [
        { key: 'progress_summary', label: 'Progress Summary', colorClass: 'consumed-card' },
        { key: 'tips_to_improve', label: 'Tips to Improve', colorClass: 'burned-card' },
        { key: 'what_to_avoid', label: 'What to Avoid', colorClass: 'bmr-card' },
        { key: 'next_steps', label: 'Next Steps', colorClass: 'tef-card' },
        { key: 'motivation_note', label: 'Motivation Note', colorClass: '', span: true }
      ];
      
      sections.forEach(s => {
        const card = document.createElement('div');
        card.className = `cal-detail-card ${s.colorClass}`;
        if (s.span) {
          card.style.gridColumn = 'span 2';
          card.style.borderColor = 'rgba(255, 255, 255, 0.15)';
        }
        
        const titleSpan = document.createElement('span');
        titleSpan.className = 'lbl';
        titleSpan.textContent = s.label;
        
        const contentSpan = document.createElement('span');
        contentSpan.className = 'val';
        contentSpan.style.fontSize = '13px';
        contentSpan.style.fontWeight = '400';
        contentSpan.style.lineHeight = '1.4';
        contentSpan.style.marginTop = '6px';
        contentSpan.style.whiteSpace = 'pre-wrap';
        contentSpan.textContent = data[s.key] || 'No insights available.';
        
        card.appendChild(titleSpan);
        card.appendChild(contentSpan);
        contentEl.appendChild(card);
      });
      contentEl.style.display = 'grid';
    }
  } catch (e) {
    console.error('fetchInsights error:', e);
    placeholderEl.innerHTML = `<p class="coach-placeholder-text" style="color: var(--color-red);">Insights unavailable right now. Please try again later.</p>`;
    placeholderEl.style.display = 'block';
  } finally {
    loadingEl.style.display = 'none';
    getInsightsBtn.disabled = false;
  }
}

async function fetchNutritionHistoryAndDraw() {
  try {
    const res = await fetch('/nutrition/history?days=7');
    if (res.ok) {
      const data = await res.json();
      drawMacrosChart(data);
      drawFiberChart(data);
    }
  } catch (e) {
    console.error('fetchNutritionHistoryAndDraw error:', e);
  }
}

function drawMacrosChart(data) {
  const canvas = document.getElementById('macrosChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Prepare last 7 days including empty days
  const prepData = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    const dateStr = d.toISOString().split('T')[0];
    const found = data.find(item => item.date === dateStr);
    if (found) {
      prepData.push(found);
    } else {
      prepData.push({
        date: dateStr,
        protein_g: 0.0,
        carbs_g: 0.0,
        fat_g: 0.0
      });
    }
  }

  const pL = 45, pR = 20, pT = 25, pB = 35;
  const gW = canvas.width - pL - pR;
  const gH = canvas.height - pT - pB;

  // Find max stacked macro height
  let maxStacked = 0;
  prepData.forEach(d => {
    const sum = (d.protein_g || 0) + (d.carbs_g || 0) + (d.fat_g || 0);
    if (sum > maxStacked) maxStacked = sum;
  });
  if (maxStacked < 100) maxStacked = 100; // default minimum ceiling
  maxStacked = Math.ceil(maxStacked / 20) * 20; // round up to multiple of 20

  // Draw axis lines
  ctx.strokeStyle = '#2c2c2c'; ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(pL, pT);
  ctx.lineTo(pL, canvas.height - pB);
  ctx.lineTo(canvas.width - pR, canvas.height - pB);
  ctx.stroke();

  // Y-axis labels and grid lines
  ctx.fillStyle = '#aaaaaa'; ctx.font = '10px Inter';
  ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
  for (let i = 0; i <= 4; i++) {
    const yVal = (maxStacked * i) / 4;
    const yPos = canvas.height - pB - (i / 4) * gH;
    ctx.strokeStyle = '#1f1f1f';
    ctx.beginPath(); ctx.moveTo(pL, yPos); ctx.lineTo(canvas.width - pR, yPos); ctx.stroke();
    ctx.fillText(Math.round(yVal) + 'g', pL - 8, yPos);
  }

  const spacing = gW / 7;
  const barW = spacing * 0.6;

  prepData.forEach((d, i) => {
    const xCenter = pL + i * spacing + spacing / 2;
    const xLeft = xCenter - barW / 2;

    // Draw faint vertical day gridline
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(xCenter, pT);
    ctx.lineTo(xCenter, canvas.height - pB);
    ctx.stroke();

    const p = d.protein_g || 0;
    const c = d.carbs_g || 0;
    const f = d.fat_g || 0;
    const total = p + c + f;

    if (total > 0) {
      const hP = (p / maxStacked) * gH;
      const hC = (c / maxStacked) * gH;
      const hF = (f / maxStacked) * gH;

      // 1. Protein (Blue)
      const yP = canvas.height - pB - hP;
      ctx.fillStyle = '#89b4fa';
      if (hP > 0) ctx.fillRect(xLeft, yP, barW, hP);

      // 2. Carbs (Amber/Yellow)
      const yC = yP - hC;
      ctx.fillStyle = '#f9e2af';
      if (hC > 0) ctx.fillRect(xLeft, yC, barW, hC);

      // 3. Fat (Peach)
      const yF = yC - hF;
      ctx.fillStyle = '#fab387';
      if (hF > 0) ctx.fillRect(xLeft, yF, barW, hF);

      ctx.fillStyle = '#ffffff';
      ctx.font = '9px Inter';
      ctx.textAlign = 'center';
      ctx.fillText(Math.round(total) + 'g', xCenter, yF - 5);
    } else {
      // Empty-state handling: subtle placeholder bar and tick
      ctx.fillStyle = 'rgba(255, 255, 255, 0.05)';
      ctx.fillRect(xLeft, canvas.height - pB - 4, barW, 4);
      
      ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
      ctx.font = '9px Inter';
      ctx.textAlign = 'center';
      ctx.fillText('-', xCenter, canvas.height - pB - 8);
    }

    // Date label
    ctx.fillStyle = '#aaaaaa'; ctx.font = '9px Inter'; ctx.textAlign = 'center';
    const parts = d.date.split('-');
    ctx.fillText(`${parts[1]}/${parts[2]}`, xCenter, canvas.height - pB + 15);
  });
}

function drawFiberChart(data) {
  const canvas = document.getElementById('fiberChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Prepare last 7 days including empty days
  const prepData = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    const dateStr = d.toISOString().split('T')[0];
    const found = data.find(item => item.date === dateStr);
    if (found) {
      prepData.push(found);
    } else {
      prepData.push({
        date: dateStr,
        fiber_g: 0.0
      });
    }
  }

  const pL = 45, pR = 20, pT = 25, pB = 35;
  const gW = canvas.width - pL - pR;
  const gH = canvas.height - pT - pB;

  // Find max fiber height
  let maxFiber = 0;
  prepData.forEach(d => {
    if (d.fiber_g > maxFiber) maxFiber = d.fiber_g;
  });
  if (maxFiber < 30) maxFiber = 30; // default minimum ceiling to display 20g target clearly
  maxFiber = Math.ceil(maxFiber / 10) * 10;

  // Draw axis lines
  ctx.strokeStyle = '#2c2c2c'; ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(pL, pT);
  ctx.lineTo(pL, canvas.height - pB);
  ctx.lineTo(canvas.width - pR, canvas.height - pB);
  ctx.stroke();

  // Y-axis labels and grid lines
  ctx.fillStyle = '#aaaaaa'; ctx.font = '10px Inter';
  ctx.textAlign = 'right'; ctx.textBaseline = 'middle';
  for (let i = 0; i <= 4; i++) {
    const yVal = (maxFiber * i) / 4;
    const yPos = canvas.height - pB - (i / 4) * gH;
    ctx.strokeStyle = '#1f1f1f';
    ctx.beginPath(); ctx.moveTo(pL, yPos); ctx.lineTo(canvas.width - pR, yPos); ctx.stroke();
    ctx.fillText(Math.round(yVal) + 'g', pL - 8, yPos);
  }

  // Draw 20g Guideline (Green dashed line)
  const yGuide = canvas.height - pB - (20.0 / maxFiber) * gH;
  ctx.strokeStyle = 'rgba(166, 227, 161, 0.4)';
  ctx.lineWidth = 1.5;
  ctx.setLineDash([5, 5]);
  ctx.beginPath();
  ctx.moveTo(pL, yGuide);
  ctx.lineTo(canvas.width - pR, yGuide);
  ctx.stroke();
  ctx.setLineDash([]); // reset dash

  ctx.fillStyle = '#a6e3a1'; ctx.font = '9px Inter'; ctx.textAlign = 'left';
  ctx.fillText('20g guideline', pL + 5, yGuide - 4);

  const spacing = gW / 7;
  const points = prepData.map((d, idx) => ({
    x: pL + idx * spacing + spacing / 2,
    y: canvas.height - pB - ((d.fiber_g || 0.0) / maxFiber) * gH,
    date: d.date,
    val: d.fiber_g || 0.0
  }));

  // Fill area under trend line
  if (points.length > 1) {
    ctx.fillStyle = 'rgba(249, 226, 175, 0.07)';
    ctx.beginPath();
    ctx.moveTo(points[0].x, canvas.height - pB);
    points.forEach(p => ctx.lineTo(p.x, p.y));
    ctx.lineTo(points[points.length - 1].x, canvas.height - pB);
    ctx.closePath(); ctx.fill();
  }

  // Draw trend line
  ctx.strokeStyle = '#f9e2af'; ctx.lineWidth = 2.5;
  ctx.beginPath();
  points.forEach((p, i) => {
    if (i === 0) ctx.moveTo(p.x, p.y);
    else ctx.lineTo(p.x, p.y);
  });
  ctx.stroke();

  // Draw vertical gridlines and dots
  points.forEach(p => {
    // Draw vertical day gridline
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(p.x, pT);
    ctx.lineTo(p.x, canvas.height - pB);
    ctx.stroke();

    const isZero = p.val === 0.0;
    
    ctx.fillStyle = isZero ? 'rgba(255, 255, 255, 0.1)' : '#ffffff';
    ctx.beginPath(); ctx.arc(p.x, p.y, isZero ? 2.5 : 4, 0, 2 * Math.PI); ctx.fill();
    
    ctx.strokeStyle = isZero ? 'rgba(255, 255, 255, 0.2)' : '#f9e2af';
    ctx.lineWidth = 1.5; ctx.stroke();

    ctx.fillStyle = '#aaaaaa'; ctx.font = '9px Inter'; ctx.textAlign = 'center';
    const parts = p.date.split('-');
    ctx.fillText(`${parts[1]}/${parts[2]}`, p.x, canvas.height - pB + 15);

    if (!isZero) {
      ctx.fillStyle = '#ffffff';
      ctx.fillText(p.val.toFixed(1) + 'g', p.x, p.y - 10);
    } else {
      ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
      ctx.fillText('-', p.x, p.y - 8);
    }
  });
}

function calculateTargetCalories(profile) {
  if (!profile || !profile.weight_kg || !profile.height_cm || !profile.age) {
    return null; // Return null to indicate incomplete profile
  }
  const weight = parseFloat(profile.weight_kg);
  const height = parseFloat(profile.height_cm);
  const age = parseInt(profile.age);
  const sex = (profile.sex || "unspecified").toLowerCase();
  
  let bmr = 0;
  if (sex === 'male' || sex === 'm') {
    bmr = 10 * weight + 6.25 * height - 5 * age + 5;
  } else if (sex === 'female' || sex === 'f') {
    bmr = 10 * weight + 6.25 * height - 5 * age - 161;
  } else {
    bmr = 10 * weight + 6.25 * height - 5 * age - 78;
  }
  
  let multiplier = 1.375;
  const freq = (profile.exercise_freq || "").toLowerCase();
  if (freq.includes("none")) {
    multiplier = 1.2;
  } else if (freq.includes("1-2") || freq.includes("1-3")) {
    multiplier = 1.375;
  } else if (freq.includes("3-5")) {
    multiplier = 1.55;
  } else if (freq.includes("daily") || freq.includes("active")) {
    multiplier = 1.725;
  }
  
  const bmrActive = bmr * multiplier;
  const neat = 75;
  const tdee = (bmrActive + neat) / 0.90;
  
  const goalType = profile.goal_type;
  if (!goalType || goalType === 'maintain') {
    return Math.max(1200, Math.round(tdee));
  }

  // Get pace percentage for calculations
  const paceVal = profile.pace || 'normal';
  let pacePct = 0.005;
  if (paceVal === 'mild') pacePct = 0.0025;
  else if (paceVal === 'aggressive') pacePct = 0.01;

  const weeklyRate = weight * pacePct;
  const dailyAdjustment = (weeklyRate * 7700) / 7;

  let target = tdee;
  if (goalType === 'lose') {
    target = tdee - dailyAdjustment;
  } else if (goalType === 'gain') {
    target = tdee + dailyAdjustment;
  }

  return Math.max(1200, Math.round(target));
}

function selectGoalTypePill(value) {
  const pills = document.querySelectorAll('.goal-type-pill');
  pills.forEach(pill => {
    if (pill.getAttribute('data-value') === value) {
      pill.classList.add('active');
    } else {
      pill.classList.remove('active');
    }
  });

  const input = document.getElementById('goalTypeSelect');
  if (input) {
    input.value = value;
  }

  // Toggle sub-options containers based on selection
  const loseGroup = document.getElementById('subLoseGroup');
  const gainGroup = document.getElementById('subGainGroup');
  const maintainGroup = document.getElementById('subMaintainGroup');
  
  if (loseGroup) loseGroup.style.display = value === 'lose' ? 'block' : 'none';
  if (gainGroup) gainGroup.style.display = value === 'gain' ? 'block' : 'none';
  if (maintainGroup) maintainGroup.style.display = value === 'maintain' ? 'block' : 'none';

  // Toggle Target Date group (always hidden for maintenance)
  const dateGroup = document.getElementById('goalTargetDateGroup');
  if (dateGroup) {
    dateGroup.style.display = value === 'maintain' ? 'none' : 'block';
  }

  const errEl = document.getElementById('goalValidationError');
  if (errEl) {
    errEl.style.display = 'none';
    errEl.textContent = '';
  }

  // Update real-time Rate / Completion projections
  updateGoalTimelineProjection();
}

function selectGoalSubOption(type, value) {
  const pills = document.querySelectorAll(`.goal-sub-pill[data-type="${type}"]`);
  pills.forEach(pill => {
    if (pill.getAttribute('data-value') === value) {
      pill.classList.add('active');
    } else {
      pill.classList.remove('active');
    }
  });

  let inputId = '';
  if (type === 'pace') inputId = 'goalPaceInput';
  else if (type === 'muscle') inputId = 'goalMuscleInput';
  else if (type === 'pace_gain') inputId = 'goalPaceGainInput';
  else if (type === 'muscle_gain') inputId = 'goalMuscleGainInput';
  else if (type === 'maintain_focus') inputId = 'goalMaintainFocusInput';

  const input = document.getElementById(inputId);
  if (input) {
    input.value = value;
  }

  updateGoalTimelineProjection();
}
window.selectGoalSubOption = selectGoalSubOption;

function updateGoalTimelineProjection() {
  const goalType = document.getElementById('goalTypeSelect').value;
  const startW = parseFloat(document.getElementById('startingWeightInput').value) || 0;
  const targetW = parseFloat(document.getElementById('targetWeightInput').value) || 0;

  const projBlock = document.getElementById('goalProjectionBlock');
  if (!projBlock) return;

  if (goalType === 'maintain' || startW <= 0 || targetW <= 0) {
    projBlock.style.display = 'none';
    document.getElementById('goalTargetDateInput').value = '';
    return;
  }

  let paceVal = '';
  if (goalType === 'lose') {
    paceVal = document.getElementById('goalPaceInput').value;
  } else {
    paceVal = document.getElementById('goalPaceGainInput').value;
  }

  let pacePct = 0.005;
  if (paceVal === 'mild') pacePct = 0.0025;
  else if (paceVal === 'aggressive') pacePct = 0.01;

  // Compute pace against currentWeightVal (or starting weight if not set yet)
  const baseWeight = currentWeightVal || startW;
  const weeklyRate = baseWeight * pacePct;
  const diff = Math.abs(targetW - startW);
  const weeks = weeklyRate > 0 ? diff / weeklyRate : 0;

  const today = new Date();
  today.setDate(today.getDate() + Math.round(weeks * 7));
  const completionDateStr = today.toISOString().split('T')[0];

  document.getElementById('projWeeklyRate').textContent = `${weeklyRate.toFixed(2)} kg/week`;
  document.getElementById('projDuration').textContent = `${Math.ceil(weeks)} week(s) (${weeks.toFixed(1)} actual)`;
  document.getElementById('projTargetDate').textContent = today.toLocaleDateString(undefined, { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
  
  document.getElementById('goalTargetDateInput').value = completionDateStr;
  projBlock.style.display = 'block';
}
window.updateGoalTimelineProjection = updateGoalTimelineProjection;

function openWeightGoalModal() {
  const modal = document.getElementById('weightGoalModal');
  if (modal) {
    const defaultGoal = userGoalType || 'lose';
    document.getElementById('startingWeightInput').value = userStartingWeight || currentWeightVal || '';
    document.getElementById('targetWeightInput').value = userTargetWeight || '';
    document.getElementById('goalTargetDateInput').value = userTargetDate || '';

    selectGoalTypePill(defaultGoal);

    // Populate active sub-option selectors
    const pace = (userProfile && userProfile.pace) || 'normal';
    const muscle = (userProfile && userProfile.muscle_focus) || 'preserve';
    const maint = (userProfile && userProfile.maintenance_focus) || 'stay_fit';

    if (defaultGoal === 'lose') {
      selectGoalSubOption('pace', pace);
      selectGoalSubOption('muscle', muscle);
    } else if (defaultGoal === 'gain') {
      selectGoalSubOption('pace_gain', pace);
      selectGoalSubOption('muscle_gain', muscle === 'preserve' ? 'lean' : muscle);
    } else {
      selectGoalSubOption('maintain_focus', maint);
    }

    const errEl = document.getElementById('goalValidationError');
    if (errEl) {
      errEl.style.display = 'none';
      errEl.textContent = '';
    }

    updateGoalTimelineProjection();
    modal.classList.add('active');
  }
}

function closeWeightGoalModal() {
  const modal = document.getElementById('weightGoalModal');
  if (modal) {
    modal.classList.remove('active');
  }
}

async function saveWeightGoalForm() {
  const goalType = document.getElementById('goalTypeSelect').value;
  const startingWeight = parseFloat(document.getElementById('startingWeightInput').value) || 0.0;
  const targetWeight = parseFloat(document.getElementById('targetWeightInput').value) || 0.0;
  const targetDate = document.getElementById('goalTargetDateInput').value || null;

  let pace = null;
  let muscle = null;
  let maintFocus = null;

  if (goalType === 'lose') {
    pace = document.getElementById('goalPaceInput').value;
    muscle = document.getElementById('goalMuscleInput').value;
  } else if (goalType === 'gain') {
    pace = document.getElementById('goalPaceGainInput').value;
    muscle = document.getElementById('goalMuscleGainInput').value;
  } else if (goalType === 'maintain') {
    maintFocus = document.getElementById('goalMaintainFocusInput').value;
  }

  const errEl = document.getElementById('goalValidationError');
  if (errEl) {
    errEl.style.display = 'none';
    errEl.textContent = '';
  }

  if (startingWeight <= 0 || targetWeight <= 0) {
    const errMsg = "Please enter valid starting and target weights.";
    if (errEl) {
      errEl.textContent = errMsg;
      errEl.style.display = 'block';
    } else {
      alert(errMsg);
    }
    return;
  }

  if (goalType === 'lose' && targetWeight >= currentWeightVal) {
    const errMsg = `Target weight (${targetWeight.toFixed(1)} kg) must be less than your current weight (${currentWeightVal.toFixed(1)} kg) for a weight loss goal.`;
    if (errEl) {
      errEl.textContent = errMsg;
      errEl.style.display = 'block';
    } else {
      alert(errMsg);
    }
    return;
  }

  if (goalType === 'gain' && targetWeight <= currentWeightVal) {
    const errMsg = `Target weight (${targetWeight.toFixed(1)} kg) must be greater than your current weight (${currentWeightVal.toFixed(1)} kg) for a weight gain goal.`;
    if (errEl) {
      errEl.textContent = errMsg;
      errEl.style.display = 'block';
    } else {
      alert(errMsg);
    }
    return;
  }

  try {
    const res = await fetch('/profile/weight-goal', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        goal_type: goalType,
        target_weight_kg: targetWeight,
        starting_weight_kg: startingWeight,
        target_date: goalType === 'maintain' ? null : targetDate,
        pace: pace,
        muscle_focus: muscle,
        maintenance_focus: maintFocus
      })
    });
    if (res.ok) {
      closeWeightGoalModal();
      await refreshDashboard();
    } else {
      const err = await res.json();
      const errMsg = "Error saving goal: " + (err.detail || "Unknown error");
      if (errEl) {
        errEl.textContent = errMsg;
        errEl.style.display = 'block';
      } else {
        alert(errMsg);
      }
    }
  } catch (e) {
    console.error("Error saving goal:", e);
    const errMsg = "Failed to save goal due to network or server error.";
    if (errEl) {
      errEl.textContent = errMsg;
      errEl.style.display = 'block';
    } else {
      alert(errMsg);
    }
  }
}

async function checkWeeklyWeighIn(profile, currentWeight) {
  const banner = document.getElementById('weeklyCheckinBanner');
  const textEl = document.getElementById('weeklyCheckinText');
  if (!banner || !textEl) return;

  if (!profile || !profile.goal_type) {
    banner.style.display = 'none';
    return;
  }

  try {
    const res = await fetch('/weight/history?days=90');
    if (!res.ok) {
      banner.style.display = 'none';
      return;
    }
    
    const history = await res.json();
    if (!history || history.length === 0) {
      textEl.textContent = "You haven't logged any weight history yet — log your weight to track your goal.";
      banner.style.display = 'flex';
      return;
    }

    history.sort((a, b) => new Date(b.date) - new Date(a.date));
    
    const latestLog = history[0];
    const latestDate = new Date(latestLog.date + 'T00:00:00');
    const today = new Date();
    today.setHours(0,0,0,0);
    latestDate.setHours(0,0,0,0);
    const diffTime = today - latestDate;
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays >= 7) {
      textEl.textContent = `It's been ${diffDays} days since your last weigh-in — log your current weight to see if you're on pace.`;
      banner.style.display = 'flex';
      return;
    }

    if (history.length < 2) {
      textEl.textContent = "Goal active! Log your weight next week to check your weekly pace progress.";
      banner.style.display = 'flex';
      return;
    }

    // Filter to last 14 days for a representative change trend
    const fourteenDaysAgo = new Date();
    fourteenDaysAgo.setDate(fourteenDaysAgo.getDate() - 14);
    const recentLogs = history.filter(h => new Date(h.date) >= fourteenDaysAgo);
    
    let oldest = history[history.length - 1];
    let latest = history[0];
    if (recentLogs.length >= 2) {
      oldest = recentLogs[recentLogs.length - 1];
      latest = recentLogs[0];
    }

    const daysDiff = (new Date(latest.date + 'T00:00:00') - new Date(oldest.date + 'T00:00:00')) / (1000 * 60 * 60 * 24);
    if (daysDiff < 1) {
      textEl.textContent = "Goal active. Log weight regularly to view your pace.";
      banner.style.display = 'flex';
      return;
    }

    const weightDiff = latest.weight_kg - oldest.weight_kg;
    const actualWeeklyRate = (weightDiff / daysDiff) * 7;
    displayPaceMessage(profile, actualWeeklyRate, textEl, banner);
  } catch (e) {
    console.error('Error checking weigh-in schedule:', e);
    banner.style.display = 'none';
  }
}

function displayPaceMessage(profile, actualWeeklyRate, textEl, banner) {
  const goalType = profile.goal_type;
  const paceVal = profile.pace || 'normal';
  let pacePct = 0.005;
  if (paceVal === 'mild') pacePct = 0.0025;
  else if (paceVal === 'aggressive') pacePct = 0.01;

  const baseWeight = parseFloat(profile.weight_kg) || 75.0;
  const targetWeeklyRate = baseWeight * pacePct;

  let actualRateOfChange = 0;
  let text = '';
  
  if (goalType === 'lose') {
    actualRateOfChange = -actualWeeklyRate;
    if (actualRateOfChange >= targetWeeklyRate * 1.15) {
      text = `🔥 Ahead of pace: You are losing weight faster than your target of ${targetWeeklyRate.toFixed(2)} kg/week (actual: ${actualRateOfChange.toFixed(2)} kg/week).`;
    } else if (actualRateOfChange <= targetWeeklyRate * 0.85) {
      text = `⚠️ Behind pace: You are losing weight slower than your target of ${targetWeeklyRate.toFixed(2)} kg/week (actual: ${actualRateOfChange.toFixed(2)} kg/week).`;
    } else {
      text = `✨ On pace: You are right on target to achieve your weight loss goal! (Target: ${targetWeeklyRate.toFixed(2)} kg/week, Actual: ${actualRateOfChange.toFixed(2)} kg/week).`;
    }
  } else if (goalType === 'gain') {
    actualRateOfChange = actualWeeklyRate;
    if (actualRateOfChange >= targetWeeklyRate * 1.15) {
      text = `🔥 Ahead of pace: You are gaining weight faster than your target of ${targetWeeklyRate.toFixed(2)} kg/week (actual: ${actualRateOfChange.toFixed(2)} kg/week).`;
    } else if (actualRateOfChange <= targetWeeklyRate * 0.85) {
      text = `⚠️ Behind pace: You are gaining weight slower than your target of ${targetWeeklyRate.toFixed(2)} kg/week (actual: ${actualRateOfChange.toFixed(2)} kg/week).`;
    } else {
      text = `✨ On pace: You are right on target to achieve your weight gain goal! (Target: ${targetWeeklyRate.toFixed(2)} kg/week, Actual: ${actualRateOfChange.toFixed(2)} kg/week).`;
    }
  } else {
    const absChange = Math.abs(actualWeeklyRate);
    if (absChange <= 0.25) {
      text = `✨ On pace: You are successfully maintaining your weight within target boundaries (weekly change: ${actualWeeklyRate.toFixed(2)} kg/week).`;
    } else {
      text = `⚠️ Behind pace: Your weight has drifted recently (weekly change: ${actualWeeklyRate.toFixed(2)} kg/week). Aim to stabilize.`;
    }
  }
  
  textEl.textContent = text;
  banner.style.display = 'flex';
}

async function initStrengthAnalytics() {
  const select = document.getElementById('strengthExerciseSelect');
  if (!select) return;

  try {
    const res = await fetch('/exercises');
    if (res.ok) {
      const list = await res.json();
      select.innerHTML = '';
      
      list.forEach(ex => {
        // Exclude hold mode or cardio keys since 1RM applies to loaded rep exercises
        if (ex.mode !== 'hold') {
          const opt = document.createElement('option');
          opt.value = ex.key;
          opt.textContent = ex.display_name;
          select.appendChild(opt);
        }
      });
      
      if (select.options.length > 0) {
        // Select first one by default
        select.selectedIndex = 0;
        await fetchStrengthTrendAndDraw();
      }
    }
  } catch (e) {
    console.error('Error initializing strength select:', e);
  }

  select.addEventListener('change', fetchStrengthTrendAndDraw);
}

async function fetchStrengthTrendAndDraw() {
  const select = document.getElementById('strengthExerciseSelect');
  if (!select) return;
  const key = select.value;
  if (!key) return;

  try {
    const res = await fetch(`/analytics/strength-trend?exercise_key=${encodeURIComponent(key)}&weeks=8`);
    if (res.ok) {
      const data = await res.json();
      drawStrengthTrendChart(data);
    }
  } catch (e) {
    console.error('Error fetching strength trend data:', e);
  }
}

function drawStrengthTrendChart(data) {
  const canvas = document.getElementById('strengthTrendChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (!data || data.length === 0) {
    ctx.fillStyle = '#aaaaaa';
    ctx.font = '14px Inter';
    ctx.textAlign = 'center';
    ctx.fillText('No history data available for this exercise over the last 8 weeks.', canvas.width / 2, canvas.height / 2);
    return;
  }

  const pL = 55, pR = 55, pT = 30, pB = 40;
  const gW = canvas.width - pL - pR;
  const gH = canvas.height - pT - pB;

  // Max 1RM scale (Left Axis)
  let max1RM = 0;
  data.forEach(d => { if (d.estimated_1rm > max1RM) max1RM = d.estimated_1rm; });
  if (max1RM < 40) max1RM = 40;
  max1RM = Math.ceil(max1RM / 10) * 10;

  // Max Volume scale (Right Axis)
  let maxVol = 0;
  data.forEach(d => { if (d.volume > maxVol) maxVol = d.volume; });
  if (maxVol < 200) maxVol = 200;
  maxVol = Math.ceil(maxVol / 100) * 100;

  // Draw axis background grids
  ctx.strokeStyle = '#2c2c2c'; ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(pL, pT);
  ctx.lineTo(pL, canvas.height - pB);
  ctx.lineTo(canvas.width - pR, canvas.height - pB);
  ctx.lineTo(canvas.width - pR, pT);
  ctx.stroke();

  // Draw Y-axis gridlines and labels
  ctx.font = '10px Inter';
  ctx.textBaseline = 'middle';
  
  for (let i = 0; i <= 4; i++) {
    const yPos = canvas.height - pB - (i / 4) * gH;
    
    // Draw horizontal faint gridline
    ctx.strokeStyle = '#1e1e2e';
    ctx.beginPath(); ctx.moveTo(pL, yPos); ctx.lineTo(canvas.width - pR, yPos); ctx.stroke();

    // Left Y label (1RM - Blue)
    const yVal1RM = (max1RM * i) / 4;
    ctx.fillStyle = '#29b6f6';
    ctx.textAlign = 'right';
    ctx.fillText(Math.round(yVal1RM) + ' kg', pL - 8, yPos);

    // Right Y label (Volume - Amber)
    const yValVol = (maxVol * i) / 4;
    ctx.fillStyle = '#ffb74d';
    ctx.textAlign = 'left';
    ctx.fillText(Math.round(yValVol) + ' kg', canvas.width - pR + 8, yPos);
  }

  const spacing = gW / data.length;
  const barW = spacing * 0.4;

  // 1. Draw Volume Bars (translucent amber)
  data.forEach((d, i) => {
    const xCenter = pL + i * spacing + spacing / 2;
    const xLeft = xCenter - barW / 2;

    // Draw vertical day gridline
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.02)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(xCenter, pT);
    ctx.lineTo(xCenter, canvas.height - pB);
    ctx.stroke();

    const vol = d.volume || 0;
    if (vol > 0) {
      const hVol = (vol / maxVol) * gH;
      const yVol = canvas.height - pB - hVol;
      ctx.fillStyle = 'rgba(255, 183, 77, 0.15)'; // Translucent amber fill
      ctx.fillRect(xLeft, yVol, barW, hVol);
      ctx.strokeStyle = 'rgba(255, 183, 77, 0.4)';
      ctx.lineWidth = 1;
      ctx.strokeRect(xLeft, yVol, barW, hVol);

      // Volume label text above bar
      ctx.fillStyle = 'rgba(255, 183, 77, 0.7)';
      ctx.font = '8px Inter';
      ctx.textAlign = 'center';
      ctx.fillText(Math.round(vol), xCenter, yVol - 4);
    } else {
      // Empty bar tick
      ctx.fillStyle = 'rgba(255, 255, 255, 0.05)';
      ctx.fillRect(xLeft, canvas.height - pB - 4, barW, 4);
    }
  });

  // 2. Draw 1RM Line (Blue)
  const linePoints = [];
  data.forEach((d, i) => {
    const xCenter = pL + i * spacing + spacing / 2;
    const rm = d.estimated_1rm || 0;
    const yRM = canvas.height - pB - (rm / max1RM) * gH;
    linePoints.push({ x: xCenter, y: yRM, val: rm, date: d.week_start });
  });

  // Connect active 1RM points (skip zeros to prevent diving to bottom)
  const activePoints = linePoints.filter(p => p.val > 0);
  if (activePoints.length > 1) {
    ctx.strokeStyle = '#29b6f6';
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    activePoints.forEach((p, i) => {
      if (i === 0) ctx.moveTo(p.x, p.y);
      else ctx.lineTo(p.x, p.y);
    });
    ctx.stroke();
  }

  // 3. Draw Dots and Labels
  linePoints.forEach(p => {
    // Week start label (MM/DD) on X axis
    ctx.fillStyle = '#aaaaaa';
    ctx.font = '9px Inter';
    ctx.textAlign = 'center';
    const parts = p.date.split('-');
    ctx.fillText(`${parts[1]}/${parts[2]}`, p.x, canvas.height - pB + 15);

    if (p.val > 0) {
      // White dot with blue stroke
      ctx.fillStyle = '#ffffff';
      ctx.beginPath(); ctx.arc(p.x, p.y, 4, 0, 2 * Math.PI); ctx.fill();
      ctx.strokeStyle = '#29b6f6'; ctx.lineWidth = 1.5; ctx.stroke();

      // Bold white label above dot
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 9px Inter';
      ctx.fillText(p.val.toFixed(1), p.x, p.y - 12);
    } else {
      // Zero state indicator on line trend
      ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
      ctx.fillText('-', p.x, p.y - 8);
    }
  });
}

async function fetchFormInsights() {
  const container = document.getElementById('formInsightsContainer');
  if (!container) return;

  try {
    const res = await fetch('/analytics/form-patterns');
    if (!res.ok) return;
    const patterns = await res.json();

    const keys = Object.keys(patterns);
    if (keys.length === 0) {
      container.innerHTML = `
        <p class="coach-placeholder-text" style="text-align: center; margin: auto; padding: 15px; font-size: 0.85rem; color: var(--text-muted);">
          No form insights compiled yet. Log 5+ sets for an exercise using camera-based tracking to see patterns.
        </p>
      `;
      container.style.justifyContent = 'center';
      container.style.alignItems = 'center';
      return;
    }

    container.innerHTML = '';
    container.style.justifyContent = 'flex-start';
    container.style.alignItems = 'stretch';

    keys.forEach(key => {
      const data = patterns[key];
      const card = document.createElement('div');
      card.style.background = 'rgba(255,255,255,0.02)';
      card.style.border = '1px solid rgba(255,255,255,0.05)';
      card.style.borderRadius = '6px';
      card.style.padding = '10px 12px';
      card.style.width = '100%';
      card.style.boxSizing = 'border-box';
      
      let html = `<div style="font-weight: 700; color: #89b4fa; font-size: 0.9rem; margin-bottom: 6px;">💪 ${data.display_name}</div>`;
      
      let issues = [];
      if (data.recurring_issue) {
        issues.push(`⚠️ Recurring issue: <strong>${data.recurring_issue.rule}</strong> flagged in <strong>${data.recurring_issue.percentage.toFixed(0)}%</strong> of sets this month.`);
      }
      
      if (data.fatigue_pattern && data.fatigue_pattern.detected) {
        issues.push(`📉 Fatigue detected: Form score drops from <strong>${data.fatigue_pattern.first_half_avg.toFixed(0)}%</strong> in early sets to <strong>${data.fatigue_pattern.second_half_avg.toFixed(0)}%</strong> in later sets.`);
      }

      if (issues.length === 0) {
        issues.push(`✨ Form remains clean and consistent across all ${data.total_sets} sets logged.`);
      }

      html += `<div style="font-size: 0.82rem; color: #a6adc8; line-height: 1.4; display: flex; flex-direction: column; gap: 4px;">`;
      issues.forEach(issue => {
        html += `<div>${issue}</div>`;
      });
      html += `</div>`;
      
      card.innerHTML = html;
      container.appendChild(card);
    });

  } catch (error) {
    console.error('Error fetching form insights:', error);
  }
}
window.fetchFormInsights = fetchFormInsights;


