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
    { id: 'overview', label: 'Overview', href: '/app/overview' },
    { id: 'workout',  label: 'Workout',  href: '/app/workout'  },
    { id: 'history',  label: 'History',  href: '/app/history'  },
    { id: 'profile',  label: 'Profile',  href: '/app/profile-page' },
    { id: 'calculator', label: 'Calculator', href: '/app/calculator' },
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

    // Setup a small functional dropdown option under profile/avatar for admins to reach /admin
    if (user.is_admin) {
      const userBadge = document.querySelector('.user-badge');
      if (userBadge) {
        userBadge.id = 'userBadge';
        userBadge.style.position = 'relative';
        userBadge.style.cursor = 'pointer';

        const dropdown = document.createElement('div');
        dropdown.id = 'userDropdown';
        dropdown.style.display = 'none';
        dropdown.style.position = 'absolute';
        dropdown.style.top = '100%';
        dropdown.style.right = '0';
        dropdown.style.marginTop = '8px';
        dropdown.style.background = '#1e1e1e';
        dropdown.style.border = '1px solid var(--border-color)';
        dropdown.style.borderRadius = '8px';
        dropdown.style.padding = '8px';
        dropdown.style.zIndex = '1000';
        dropdown.style.boxShadow = '0 4px 12px rgba(0,0,0,0.5)';
        dropdown.style.minWidth = '120px';

        const adminLink = document.createElement('a');
        adminLink.href = '/admin';
        adminLink.style.display = 'block';
        adminLink.style.color = 'var(--text-main)';
        adminLink.style.textDecoration = 'none';
        adminLink.style.padding = '6px 12px';
        adminLink.style.fontSize = '13px';
        adminLink.style.borderRadius = '4px';
        adminLink.style.transition = 'background 0.2s';
        adminLink.textContent = 'Admin Panel';
        adminLink.onmouseover = () => adminLink.style.background = 'rgba(255,255,255,0.08)';
        adminLink.onmouseout = () => adminLink.style.background = 'transparent';

        dropdown.appendChild(adminLink);
        userBadge.appendChild(dropdown);

        // Toggle dropdown on click
        userBadge.addEventListener('click', (e) => {
          e.stopPropagation();
          dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
        });

        // Close dropdown when clicking elsewhere
        document.addEventListener('click', () => {
          dropdown.style.display = 'none';
        });
      }
    }

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
