// Apply theme instantly on script parse to minimize FOUC
if (localStorage.getItem('theme') === 'light') {
  document.body.classList.add('light-theme');
}

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
        <button id="themeToggleBtn" class="btn btn-secondary" style="margin-left:10px; padding: 6px; display: inline-flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 50%; border: 1px solid var(--border-color); background: var(--panel-bg); color: var(--text-main); cursor: pointer;" title="Toggle Light/Dark Mode">
          <!-- Moon Icon (Dark Mode active) -->
          <svg id="themeIconMoon" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" style="width: 18px; height: 18px;">
            <path stroke-linecap="round" stroke-linejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>
          <!-- Sun Icon (Light Mode active) -->
          <svg id="themeIconSun" class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" style="width: 18px; height: 18px; display: none;">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364-6.364l-.707.707M6.343 17.657l-.707.707m0-12.728l.707.707m12.728 12.728l.707.707M12 7a5 5 0 100 10 5 5 0 000-10z" />
          </svg>
        </button>
        <button class="btn btn-danger btn-sm" id="logoutBtn" style="margin-left:10px;">Log Out</button>
      </div>
    </header>
  `;

  const placeholder = document.getElementById('navPlaceholder');
  if (placeholder) {
    placeholder.outerHTML = navHtml;
    setupTheme();
  }

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

function setupTheme() {
  const toggleBtn = document.getElementById('themeToggleBtn');
  const moonIcon = document.getElementById('themeIconMoon');
  const sunIcon = document.getElementById('themeIconSun');

  if (!toggleBtn) return;

  // Apply current theme
  const currentTheme = localStorage.getItem('theme') || 'dark';
  if (currentTheme === 'light') {
    document.body.classList.add('light-theme');
    if (moonIcon) moonIcon.style.display = 'none';
    if (sunIcon) sunIcon.style.display = 'block';
  } else {
    document.body.classList.remove('light-theme');
    if (moonIcon) moonIcon.style.display = 'block';
    if (sunIcon) sunIcon.style.display = 'none';
  }

  // Toggle handler
  toggleBtn.onclick = () => {
    const isLight = document.body.classList.contains('light-theme');
    if (isLight) {
      document.body.classList.remove('light-theme');
      localStorage.setItem('theme', 'dark');
      if (moonIcon) moonIcon.style.display = 'block';
      if (sunIcon) sunIcon.style.display = 'none';
    } else {
      document.body.classList.add('light-theme');
      localStorage.setItem('theme', 'light');
      if (moonIcon) moonIcon.style.display = 'none';
      if (sunIcon) sunIcon.style.display = 'block';
    }
  };
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
