// FitSense AI — Shared App Logic

// ── Global 401 interceptor ──────────────────────────────────────────────────
const _originalFetch = window.fetch;
window.fetch = async function (...args) {
  const response = await _originalFetch(...args);
  const path = window.location.pathname;
  if (
    response.status === 401 &&
    !path.includes('login.html') &&
    !path.includes('register.html')
  ) {
    window.location.href = '/login.html';
  }
  return response;
};

// ── Shared state ────────────────────────────────────────────────────────────
window.activeProfile = null;

// ── Nav injection ───────────────────────────────────────────────────────────
function injectNav(activePage) {
  const pages = [
    { id: 'overview', label: 'Overview', href: '/overview' },
    { id: 'workout',  label: 'Workout',  href: '/workout'  },
    { id: 'history',  label: 'History',  href: '/history'  },
    { id: 'profile',  label: 'Profile',  href: '/profile-page' },
    { id: 'calculator', label: 'Calculator', href: '/calculator' },
  ];

  const navHtml = `
    <header class="app-header" id="appHeader">
      <div class="logo-area">
        <span class="logo-accent">FitSense</span> <span class="logo-sub">AI</span>
      </div>
      <nav class="main-nav" id="mainNav">
        ${pages.map(p => `
          <a href="${p.href}" class="nav-link${p.id === activePage ? ' active' : ''}">${p.label}</a>
        `).join('')}
      </nav>
      <div class="header-right">
        <a href="/admin" class="btn btn-secondary btn-sm" id="adminHeaderBtn" style="display:none;text-decoration:none;">Admin</a>
        <div class="user-badge">
          <div class="avatar" id="avatarBadge">A</div>
          <span id="username">Athlete</span>
        </div>
        <button class="btn btn-danger btn-sm" id="logoutBtn" style="margin-left:10px;">Log Out</button>
      </div>
    </header>
  `;

  const placeholder = document.getElementById('navPlaceholder');
  if (placeholder) placeholder.outerHTML = navHtml;

  // Logout handler
  document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', async () => {
        try {
          const res = await fetch('/api/auth/logout', { method: 'POST' });
          if (res.ok) window.location.href = '/login.html';
        } catch (e) {
          console.error('Logout error:', e);
        }
      });
    }
  });
}

// ── Auth + user init ────────────────────────────────────────────────────────
async function initAuth() {
  try {
    const res = await fetch('/api/auth/me');
    if (!res.ok) { window.location.href = '/login.html'; return null; }
    const user = await res.json();

    const usernameEl = document.getElementById('username');
    const avatarEl   = document.getElementById('avatarBadge');
    if (usernameEl) usernameEl.textContent = user.name || 'Athlete';
    if (avatarEl)   avatarEl.textContent   = user.name ? user.name[0].toUpperCase() : 'U';

    const adminBtn = document.getElementById('adminHeaderBtn');
    if (adminBtn && user.is_admin) adminBtn.style.display = 'inline-flex';

    return user;
  } catch (e) {
    console.error('Auth error:', e);
    window.location.href = '/login.html';
    return null;
  }
}

// ── Profile fetch ───────────────────────────────────────────────────────────
async function fetchProfile() {
  try {
    const res = await fetch('/profile');
    if (res.ok) {
      window.activeProfile = await res.json();

      const usernameEl = document.getElementById('username');
      const avatarEl   = document.getElementById('avatarBadge');
      if (usernameEl && window.activeProfile.name)
        usernameEl.textContent = window.activeProfile.name;
      if (avatarEl && window.activeProfile.name)
        avatarEl.textContent = window.activeProfile.name[0].toUpperCase();
    }
  } catch (e) {
    console.error('fetchProfile error:', e);
  }
}

// ── Score helpers ───────────────────────────────────────────────────────────
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
function getBadgeClass(severity) {
  if (severity === 'RED')    return 'badge-red';
  if (severity === 'YELLOW') return 'badge-yellow';
  return 'badge-green';
}
