// FitSense AI — History Page Logic

document.addEventListener('DOMContentLoaded', async () => {
  injectNav('history');
  const user = await initAuth();
  if (!user) return;

  setupEventListeners();
  await fetchRecentSessions();
});

function setupEventListeners() {
  document.getElementById('closeDetailBtn').addEventListener('click', () => {
    document.getElementById('detailModal').classList.remove('active');
  });
}

async function fetchRecentSessions() {
  const historyBody = document.getElementById('historyBody');
  try {
    const res = await fetch('/sessions/recent');
    const sessions = await res.json();

    if (sessions.length === 0) {
      historyBody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: #aaaaaa; padding: 30px 0;">No sessions yet — start a workout to see your stats here</td></tr>`;
      return;
    }

    historyBody.innerHTML = '';
    sessions.forEach(sess => {
      const dateFormatted = new Date(sess.date).toLocaleDateString(undefined, {
        year: 'numeric', month: 'short', day: 'numeric'
      });

      const repsOrTime = sess.exercises_done &&
        (sess.exercises_done.includes('Plank') || sess.exercises_done.includes('Hold') || sess.exercises_done.includes('Sit'))
        ? `${Math.round(sess.total_reps)}s`
        : sess.total_reps;

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>${dateFormatted}</td>
        <td>${sess.exercises_done || 'None'}</td>
        <td>${sess.total_sets}</td>
        <td>${repsOrTime}</td>
        <td>${sess.total_calories_burned ? sess.total_calories_burned.toFixed(1) + ' kcal' : '0 kcal'}</td>
        <td><span class="${getScoreColorClass(sess.avg_form_score)}">${Math.round(sess.avg_form_score)}%</span></td>
        <td><span class="view-link" onclick="viewSessionDetails(${sess.session_id})">View Detail</span></td>
      `;
      historyBody.appendChild(tr);
    });
  } catch (e) {
    console.error('fetchRecentSessions error:', e);
    historyBody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: #ff5252;">Failed to load history.</td></tr>`;
  }
}

async function viewSessionDetails(sessionId) {
  try {
    const res = await fetch(`/sessions/${sessionId}`);
    const detail = await res.json();
    if (!detail) return;

    const dateFormatted = new Date(detail.date).toLocaleDateString(undefined, {
      year: 'numeric', month: 'short', day: 'numeric'
    });

    document.getElementById('detailTitle').textContent = `Workout Session Details #${detail.session_id}`;
    document.getElementById('detDate').textContent     = dateFormatted;
    document.getElementById('detDuration').textContent = detail.total_duration_mins ? detail.total_duration_mins.toFixed(1) : '0';
    document.getElementById('detCalories').textContent = detail.total_calories_burned ? detail.total_calories_burned.toFixed(1) : '0';
    document.getElementById('detForm').textContent     = Math.round(detail.avg_form_score);
    document.getElementById('detNotes').textContent    = detail.notes || 'No notes added.';

    const detailSetsBody = document.getElementById('detailSetsBody');
    detailSetsBody.innerHTML = '';
    if (detail.exercises) {
      detail.exercises.forEach(ex => {
        const isExHold = ex.exercise_key.includes('plank') || ex.exercise_key.includes('sit') || ex.exercise_key.includes('hold');
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
              <td>${set.pain_flag ? `<span class="score-red">YES (${set.pain_location || 'N/A'})</span>` : 'No'}</td>
            `;
            detailSetsBody.appendChild(tr);
          });
        }
      });
    }

    if (detailSetsBody.innerHTML === '') {
      detailSetsBody.innerHTML = '<tr><td colspan="7" style="text-align: center;">No sets found for this session.</td></tr>';
    }

    document.getElementById('detailModal').classList.add('active');
  } catch (e) {
    console.error('viewSessionDetails error:', e);
  }
}
