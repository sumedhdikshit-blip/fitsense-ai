// FitSense AI — Calculator Page Logic

let lastResult = null;

document.addEventListener('DOMContentLoaded', async () => {
  injectNav('calculator');
  const user = await initAuth();
  if (!user) return;

  await prefillFromProfile();

  document.getElementById('calculatorForm').addEventListener('submit', runCalculation);
});

async function prefillFromProfile() {
  await fetchProfile();
  const p = window.activeProfile;
  if (!p) return;
  if (p.weight_kg) document.getElementById('calcWeight').value = p.weight_kg;
  if (p.height_cm) document.getElementById('calcHeight').value = p.height_cm;
  if (p.age) document.getElementById('calcAge').value = p.age;
  if (p.sex) {
    const sex = p.sex.toLowerCase();
    if (['male', 'female', 'unspecified', 'other'].includes(sex)) {
      document.getElementById('calcGender').value = sex === 'female' ? 'female' : (sex === 'male' ? 'male' : 'other');
    }
  }
}

function runCalculation(e) {
  e.preventDefault();

  const weight = parseFloat(document.getElementById('calcWeight').value);
  const height = parseFloat(document.getElementById('calcHeight').value);
  const age = parseInt(document.getElementById('calcAge').value);
  const gender = document.getElementById('calcGender').value;
  const protein = parseFloat(document.getElementById('calcProtein').value) || 0;
  const activityMultiplier = parseFloat(document.getElementById('calcActivity').value);

  // 1. BMI
  const bmi = weight / ((height / 100) ** 2);

  // 2. BMR (Mifflin-St Jeor)
  let bmr = 0;
  if (gender === 'male') {
    bmr = 10 * weight + 6.25 * height - 5 * age + 5;
  } else if (gender === 'female') {
    bmr = 10 * weight + 6.25 * height - 5 * age - 161;
  } else {
    // Average of male and female
    const maleBmr = 10 * weight + 6.25 * height - 5 * age + 5;
    const femaleBmr = 10 * weight + 6.25 * height - 5 * age - 161;
    bmr = (maleBmr + femaleBmr) / 2;
  }

  // 3. NEAT (Non-Exercise Activity Thermogenesis flat incidental estimate)
  const neat = 75; // midpoint of 50-100 kcal

  // 4. TDEE and TEF
  // TDEE = (BMR_active + NEAT) / 0.90
  // TEF = 10% of TDEE
  const bmrActive = bmr * activityMultiplier;
  const tdee = (bmrActive + neat) / 0.90;
  const tef = tdee * 0.10;

  const currentResult = {
    bmi: bmi.toFixed(1),
    bmr: Math.round(bmr),
    tef: Math.round(tef),
    neat: Math.round(neat),
    tdee: Math.round(tdee)
  };

  // If there was a previous calculation, populate the previous container
  if (lastResult) {
    document.getElementById('prevBmi').textContent = lastResult.bmi;
    document.getElementById('prevBmr').textContent = `${lastResult.bmr} kcal`;
    document.getElementById('prevTef').textContent = `${lastResult.tef} kcal`;
    document.getElementById('prevNeat').textContent = `${lastResult.neat} kcal`;
    document.getElementById('prevTdee').textContent = `${lastResult.tdee} kcal`;
    document.getElementById('previousResults').style.display = 'block';
  }

  // Update current results UI
  document.getElementById('valBmi').textContent = currentResult.bmi;
  document.getElementById('valBmr').textContent = `${currentResult.bmr} kcal`;
  document.getElementById('valTef').textContent = `${currentResult.tef} kcal`;
  document.getElementById('valNeat').textContent = `${currentResult.neat} kcal`;
  document.getElementById('valTdee').textContent = `${currentResult.tdee} kcal`;

  document.getElementById('noResultsMsg').style.display = 'none';
  document.getElementById('currentResults').style.display = 'block';

  // Store this run as lastResult
  lastResult = currentResult;
}
