// FitSense AI — Profile Page Logic

document.addEventListener('DOMContentLoaded', async () => {
  injectNav('profile');
  const user = await initAuth();
  if (!user) return;

  await loadProfileIntoForm();

  document.getElementById('saveProfileBtn').addEventListener('click', saveProfile);
  document.getElementById('estimateRiskBtn').addEventListener('click', calculateRiskEstimate);
});

async function loadProfileIntoForm() {
  await fetchProfile();
  const p = window.activeProfile;
  if (!p) return;

  document.getElementById('profileName').value   = p.name || '';
  document.getElementById('profileAge').value    = p.age || '';
  document.getElementById('profileSex').value    = p.sex || 'unspecified';
  document.getElementById('profileWeight').value = p.weight_kg || '';
  document.getElementById('profileHeight').value = p.height_cm || '';
  document.getElementById('profileGoal').value   = p.fitness_goal || '';

  // Load new health fields
  document.getElementById('profileGender').value       = p.gender || '';
  document.getElementById('profileSmoker').value       = p.smoker || '';
  document.getElementById('profileSleep').value        = p.sleep_hours !== null && p.sleep_hours !== undefined ? p.sleep_hours : '';
  document.getElementById('profileStress').value       = p.stress_level !== null && p.stress_level !== undefined ? p.stress_level : '';
  document.getElementById('profileExerciseFreq').value = p.exercise_freq || '';
  document.getElementById('profileDietQuality').value  = p.diet_quality || '';
  document.getElementById('profileAlcohol').value      = p.alcohol_consumption || '';
}

async function saveProfile() {
  const sleepVal = document.getElementById('profileSleep').value;
  const stressVal = document.getElementById('profileStress').value;

  const payload = {
    name:         document.getElementById('profileName').value || 'Athlete',
    age:          parseInt(document.getElementById('profileAge').value) || 0,
    weight_kg:    parseFloat(document.getElementById('profileWeight').value) || 0.0,
    height_cm:    parseFloat(document.getElementById('profileHeight').value) || 0.0,
    sex:          document.getElementById('profileSex').value,
    fitness_goal: document.getElementById('profileGoal').value || '',
    
    // Additional parameters
    gender:       document.getElementById('profileGender').value || null,
    smoker:       document.getElementById('profileSmoker').value || null,
    sleep_hours:  sleepVal !== '' ? parseFloat(sleepVal) : null,
    stress_level: stressVal !== '' ? parseInt(stressVal) : null,
    exercise_freq: document.getElementById('profileExerciseFreq').value || null,
    diet_quality:  document.getElementById('profileDietQuality').value || null,
    alcohol_consumption: document.getElementById('profileAlcohol').value || null
  };

  try {
    const res = await fetch('/profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (res.ok) {
      await loadProfileIntoForm();
      const msg = document.getElementById('profileSavedMsg');
      msg.style.display = 'inline';
      setTimeout(() => { msg.style.display = 'none'; }, 3000);
    } else {
      const err = await res.json();
      alert(`Error: ${err.detail || 'Validation failed.'}`);
    }
  } catch (e) {
    console.error('saveProfile error:', e);
  }
}

async function calculateRiskEstimate() {
  const btn = document.getElementById('estimateRiskBtn');
  const errBox = document.getElementById('riskErrorBox');
  const resBox = document.getElementById('riskResultBox');
  const probVal = document.getElementById('riskProbabilityVal');
  const classBadge = document.getElementById('riskClassBadge');
  const discBox = document.getElementById('riskConfidenceDisclaimer');

  btn.disabled = true;
  btn.textContent = 'Calculating...';
  errBox.style.display = 'none';
  resBox.style.display = 'none';

  try {
    // Post empty object: the server defaults to reading columns from active profile
    const res = await fetch('/experimental/risk-estimate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({})
    });

    if (!res.ok) {
      const err = await res.json();
      // Show missing fields list
      errBox.textContent = err.detail || 'Failed to calculate risk.';
      errBox.style.display = 'block';
      return;
    }

    const result = await res.json();
    
    // Display risk results
    const riskPercent = Math.round(result.predicted_probability * 100);
    probVal.textContent = `${riskPercent}%`;
    classBadge.textContent = result.predicted_class ? 'Elevated Indicator' : 'Baseline Indicator';
    
    // Inject confidence note prominently
    discBox.textContent = result.confidence_note;
    
    resBox.style.display = 'block';

  } catch (e) {
    console.error('calculateRiskEstimate error:', e);
    errBox.textContent = 'An unexpected network error occurred.';
    errBox.style.display = 'block';
  } finally {
    btn.disabled = false;
    btn.textContent = '📊 Calculate Exploratory Estimate';
  }
}

