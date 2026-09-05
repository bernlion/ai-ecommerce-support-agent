const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new Error(data.detail || 'Request failed. Please try again.');
  }
  return response.json();
}

export function sendChat(customerId, message) {
  return request('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ customer_id: customerId, message }),
  });
}

export function getHealth() {
  return request('/api/health');
}
