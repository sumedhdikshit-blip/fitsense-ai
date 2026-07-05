// FitSense AI — Profile Page Logic

document.addEventListener('DOMContentLoaded', async () => {
  injectNav('profile');
  const user = await initAuth();
  if (!user) return;

  await loadProfileIntoForm();

  document.getElementById('saveProfileBtn').addEventListener('click', saveProfile);
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
}

async function saveProfile() {
  const payload = {
    name:         document.getElementById('profileName').value || 'Athlete',
    age:          parseInt(document.getElementById('profileAge').value) || 0,
    weight_kg:    parseFloat(document.getElementById('profileWeight').value) || 0.0,
    height_cm:    parseFloat(document.getElementById('profileHeight').value) || 0.0,
    sex:          document.getElementById('profileSex').value,
    fitness_goal: document.getElementById('profileGoal').value || ''
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
      alert(`Error: ${err.detail || 'Validation failed. Age 1-120, Weight 10-500, Height 50-300.'}`);
    }
  } catch (e) {
    console.error('saveProfile error:', e);
  }
}
