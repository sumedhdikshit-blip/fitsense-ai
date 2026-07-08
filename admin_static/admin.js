// FitSense AI - Admin Dashboard Script
const usersTableBody = document.getElementById('usersTableBody');
const totalUsersVal = document.getElementById('totalUsersVal');
const totalSessionsVal = document.getElementById('totalSessionsVal');
const lastActivityVal = document.getElementById('lastActivityVal');
const logoutBtn = document.getElementById('logoutBtn');

// Fetch user diagnostic statistics
async function loadDiagnostics() {
  try {
    const response = await fetch('/api/admin/users');
    if (response.status === 401) {
      window.location.href = '/login.html';
      return;
    } else if (response.status === 403) {
      usersTableBody.innerHTML = `<tr><td colspan="6" class="table-loading" style="color: var(--danger-color); font-weight: 600;">Access Denied: Admin privileges required.</td></tr>`;
      return;
    }

    const data = await response.json();
    if (data.length === 0) {
      usersTableBody.innerHTML = '<tr><td colspan="6" class="table-loading">No registered users found.</td></tr>';
      return;
    }

    // Populate Metrics Grid
    totalUsersVal.textContent = data.length;
    
    const sumSessions = data.reduce((acc, user) => acc + (user.total_sessions || 0), 0);
    totalSessionsVal.textContent = sumSessions;

    // Find the latest active user
    let latestUser = null;
    let latestTime = null;
    data.forEach(user => {
      if (user.last_active_date) {
        const timeVal = new Date(user.last_active_date).getTime();
        if (!latestTime || timeVal > latestTime) {
          latestTime = timeVal;
          latestUser = user;
        }
      }
    });

    if (latestUser) {
      const activeDateStr = latestUser.last_active_date.split('T')[0];
      lastActivityVal.textContent = `${latestUser.name} (${activeDateStr})`;
    } else {
      lastActivityVal.textContent = 'None';
    }

    // Populate Table
    usersTableBody.innerHTML = '';
    data.forEach(user => {
      const tr = document.createElement('tr');
      const lastActive = user.last_active_date ? user.last_active_date.replace('T', ' ') : '--';
      const roleBadge = user.is_admin 
        ? '<span class="badge badge-blue">ADMIN</span>' 
        : '<span class="badge badge-slate">USER</span>';

      tr.innerHTML = `
        <td><strong>${user.user_id}</strong></td>
        <td>${user.username}</td>
        <td>${user.name}</td>
        <td>${roleBadge}</td>
        <td>${user.total_sessions}</td>
        <td>${lastActive}</td>
      `;
      usersTableBody.appendChild(tr);
    });
  } catch (error) {
    console.error('Error fetching admin summary:', error);
    usersTableBody.innerHTML = '<tr><td colspan="6" class="table-loading" style="color: var(--danger-color);">Failed to load system diagnostics.</td></tr>';
  }
}

// Log Out Handler
logoutBtn.addEventListener('click', async () => {
  try {
    const response = await fetch('/api/auth/logout', { method: 'POST' });
    if (response.ok) {
      window.location.href = '/login.html';
    }
  } catch (error) {
    console.error('Logout error:', error);
  }
});

// Run diagnostics on load
loadDiagnostics();
