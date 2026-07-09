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
    injectChatbot();
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

function injectChatbot() {
  // Avoid duplicate injection
  if (document.getElementById('fitsenseChatWidget')) return;

  const widget = document.createElement('div');
  widget.id = 'fitsenseChatWidget';
  widget.className = 'fitsense-chat-widget';
  
  widget.innerHTML = `
    <div class="fitsense-chat-bubble" id="fitsenseChatBubble" title="Chat with FitSense Assistant">
      <div class="fitsense-chat-badge" id="fitsenseChatBadge"></div>
      <svg viewBox="0 0 24 24">
        <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
      </svg>
    </div>
    <div class="fitsense-chat-panel" id="fitsenseChatPanel">
      <div class="fitsense-chat-header">
        <div class="fitsense-chat-header-title">
          <div class="fitsense-chat-bot-icon">
            <svg viewBox="0 0 24 24"><path fill="currentColor" d="M19 8h-1.18c-.48-2.31-2.51-4-4.82-4s-4.34 1.69-4.82 4H7c-1.1 0-2 .9-2 2v3c0 1.1.9 2 2 2h.18c.48 2.31 2.51 4 4.82 4s4.34-1.69 4.82-4H17c1.1 0 2-.9 2-2v-3c0-1.1-.9-2-2-2zm-7 10c-2.21 0-4-1.79-4-4h8c0 2.21-1.79 4-4 4zm4-6c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm-8 0c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z"/></svg>
          </div>
          <div class="fitsense-chat-header-text">
            <span class="fitsense-chat-title-main">FitSense Assistant</span>
            <span class="fitsense-chat-title-sub"><span class="fitsense-chat-status-dot"></span>Online</span>
          </div>
        </div>
        <button class="fitsense-chat-close" id="fitsenseChatClose" title="Minimize">
          <svg viewBox="0 0 24 24"><path fill="currentColor" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/></svg>
        </button>
      </div>
      <div class="fitsense-chat-messages" id="fitsenseChatMessages"></div>
      <div class="fitsense-chat-input-area">
        <input type="text" class="fitsense-chat-input" id="fitsenseChatInput" placeholder="Ask about fitness, nutrition, goals..." autocomplete="off">
        <button class="fitsense-chat-send-btn" id="fitsenseChatSendBtn" title="Send Message">
          <svg viewBox="0 0 24 24"><path fill="currentColor" d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
        </button>
      </div>
    </div>
  `;

  document.body.appendChild(widget);

  const bubble = document.getElementById('fitsenseChatBubble');
  const panel = document.getElementById('fitsenseChatPanel');
  const closeBtn = document.getElementById('fitsenseChatClose');
  const input = document.getElementById('fitsenseChatInput');
  const sendBtn = document.getElementById('fitsenseChatSendBtn');
  const messagesContainer = document.getElementById('fitsenseChatMessages');

  let history = [];
  try {
    const storedHistory = sessionStorage.getItem('fitsense_chat_history');
    if (storedHistory) {
      history = JSON.parse(storedHistory);
    }
  } catch (e) {
    console.error('Error loading chat history from sessionStorage', e);
  }

  // Restore open state
  const isOpen = sessionStorage.getItem('fitsense_chat_open') === 'true';
  if (isOpen) {
    panel.style.display = 'flex';
    panel.classList.add('open');
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Render conversation history
  function renderMessages() {
    messagesContainer.innerHTML = '';
    
    // Welcome message
    const welcomeMsg = document.createElement('div');
    welcomeMsg.className = 'fitsense-chat-msg fitsense-chat-msg-bot';
    welcomeMsg.innerHTML = `
      <div class="fitsense-chat-avatar">
        <svg viewBox="0 0 24 24"><path fill="currentColor" d="M19 8h-1.18c-.48-2.31-2.51-4-4.82-4s-4.34 1.69-4.82 4H7c-1.1 0-2 .9-2 2v3c0 1.1.9 2 2 2h.18c.48 2.31 2.51 4 4.82 4s4.34-1.69 4.82-4H17c1.1 0 2-.9 2-2v-3c0-1.1-.9-2-2-2zm-7 10c-2.21 0-4-1.79-4-4h8c0 2.21-1.79 4-4 4zm4-6c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm-8 0c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z"/></svg>
      </div>
      <div class="fitsense-chat-msg-text">Hi! I am your FitSense Coach. Ask me any questions about fitness, nutrition, workouts, or goals!</div>
    `;
    messagesContainer.appendChild(welcomeMsg);

    history.forEach(msg => {
      const msgDiv = document.createElement('div');
      msgDiv.className = `fitsense-chat-msg fitsense-chat-msg-${msg.role === 'user' ? 'user' : 'bot'}`;
      if (msg.role === 'user') {
        msgDiv.innerHTML = `<div class="fitsense-chat-msg-text">${escapeHtml(msg.content)}</div>`;
      } else {
        msgDiv.innerHTML = `
          <div class="fitsense-chat-avatar">
            <svg viewBox="0 0 24 24"><path fill="currentColor" d="M19 8h-1.18c-.48-2.31-2.51-4-4.82-4s-4.34 1.69-4.82 4H7c-1.1 0-2 .9-2 2v3c0 1.1.9 2 2 2h.18c.48 2.31 2.51 4 4.82 4s4.34-1.69 4.82-4H17c1.1 0 2-.9 2-2v-3c0-1.1-.9-2-2-2zm-7 10c-2.21 0-4-1.79-4-4h8c0 2.21-1.79 4-4 4zm4-6c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm-8 0c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z"/></svg>
          </div>
          <div class="fitsense-chat-msg-text">${escapeHtml(msg.content)}</div>
        `;
      }
      messagesContainer.appendChild(msgDiv);
    });

    scrollToBottom();
  }

  function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  // Toggle open
  bubble.onclick = (e) => {
    e.stopPropagation();
    const willOpen = !panel.classList.contains('open');
    if (willOpen) {
      panel.style.display = 'flex';
      // Force repaint to allow transition
      panel.offsetHeight;
      panel.classList.add('open');
      sessionStorage.setItem('fitsense_chat_open', 'true');
      input.focus();
      scrollToBottom();
      // Hide badge
      const badge = document.getElementById('fitsenseChatBadge');
      if (badge) badge.classList.remove('visible');
    } else {
      panel.classList.remove('open');
      sessionStorage.setItem('fitsense_chat_open', 'false');
      setTimeout(() => {
        if (!panel.classList.contains('open')) {
          panel.style.display = 'none';
        }
      }, 220);
    }
  };

  // Close/Minimize
  closeBtn.onclick = (e) => {
    e.stopPropagation();
    panel.classList.remove('open');
    sessionStorage.setItem('fitsense_chat_open', 'false');
    setTimeout(() => {
      if (!panel.classList.contains('open')) {
        panel.style.display = 'none';
      }
    }, 220);
  };

  // Message sending
  async function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    input.value = '';
    
    // Add User Message
    history.push({ role: 'user', content: text });
    sessionStorage.setItem('fitsense_chat_history', JSON.stringify(history));
    
    // Render the user message immediately
    const userMsgDiv = document.createElement('div');
    userMsgDiv.className = 'fitsense-chat-msg fitsense-chat-msg-user';
    userMsgDiv.innerHTML = `<div class="fitsense-chat-msg-text">${escapeHtml(text)}</div>`;
    messagesContainer.appendChild(userMsgDiv);
    scrollToBottom();

    // Show Typing Indicator
    const typingIndicator = document.createElement('div');
    typingIndicator.id = 'fitsenseChatTyping';
    typingIndicator.className = 'fitsense-chat-typing';
    typingIndicator.innerHTML = `
      <div class="fitsense-chat-avatar">
        <svg viewBox="0 0 24 24"><path fill="currentColor" d="M19 8h-1.18c-.48-2.31-2.51-4-4.82-4s-4.34 1.69-4.82 4H7c-1.1 0-2 .9-2 2v3c0 1.1.9 2 2 2h.18c.48 2.31 2.51 4 4.82 4s4.34-1.69 4.82-4H17c1.1 0 2-.9 2-2v-3c0-1.1-.9-2-2-2zm-7 10c-2.21 0-4-1.79-4-4h8c0 2.21-1.79 4-4 4zm4-6c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm-8 0c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z"/></svg>
      </div>
      <div class="fitsense-chat-typing-dots">
        <div class="fitsense-chat-typing-dot"></div>
        <div class="fitsense-chat-typing-dot"></div>
        <div class="fitsense-chat-typing-dot"></div>
      </div>
    `;
    messagesContainer.appendChild(typingIndicator);
    scrollToBottom();

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
      });

      // Remove typing indicator
      const currentIndicator = document.getElementById('fitsenseChatTyping');
      if (currentIndicator) currentIndicator.remove();

      if (!response.ok) {
        throw new Error('API request failed');
      }

      const data = await response.json();
      
      // Add Bot Message
      history.push({ role: 'assistant', content: data.reply });
      
      // Truncate locally to match server-side history trimming (max 6 messages)
      if (history.length > 6) {
        history = history.slice(-6);
      }
      sessionStorage.setItem('fitsense_chat_history', JSON.stringify(history));

      // Append bot message to UI
      const botMsgDiv = document.createElement('div');
      botMsgDiv.className = 'fitsense-chat-msg fitsense-chat-msg-bot';
      botMsgDiv.innerHTML = `
        <div class="fitsense-chat-avatar">
          <svg viewBox="0 0 24 24"><path fill="currentColor" d="M19 8h-1.18c-.48-2.31-2.51-4-4.82-4s-4.34 1.69-4.82 4H7c-1.1 0-2 .9-2 2v3c0 1.1.9 2 2 2h.18c.48 2.31 2.51 4 4.82 4s4.34-1.69 4.82-4H17c1.1 0 2-.9 2-2v-3c0-1.1-.9-2-2-2zm-7 10c-2.21 0-4-1.79-4-4h8c0 2.21-1.79 4-4 4zm4-6c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm-8 0c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z"/></svg>
        </div>
        <div class="fitsense-chat-msg-text">${escapeHtml(data.reply)}</div>
      `;
      messagesContainer.appendChild(botMsgDiv);
      scrollToBottom();

      // Show unread badge if user closed panel while loading
      if (!panel.classList.contains('open')) {
        const badge = document.getElementById('fitsenseChatBadge');
        if (badge) badge.classList.add('visible');
      }

    } catch (err) {
      console.error('Chat failed:', err);
      // Remove typing indicator if it wasn't already removed
      const currentIndicator = document.getElementById('fitsenseChatTyping');
      if (currentIndicator) currentIndicator.remove();

      // Show Error Bubble
      const errorMsgDiv = document.createElement('div');
      errorMsgDiv.className = 'fitsense-chat-msg fitsense-chat-msg-error';
      errorMsgDiv.textContent = "Sorry, I couldn't process that — try again.";
      messagesContainer.appendChild(errorMsgDiv);
      scrollToBottom();
      
      if (!panel.classList.contains('open')) {
        const badge = document.getElementById('fitsenseChatBadge');
        if (badge) badge.classList.add('visible');
      }
    }
  }

  sendBtn.onclick = sendMessage;
  input.onkeypress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  renderMessages();
}

