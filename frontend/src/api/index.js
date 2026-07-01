/**
 * Backend API client (by business module). Base URL from env.
 */
const BASE_URL = import.meta.env?.VITE_API_BASE_URL || '/api';

export async function listAccounts(params = {}) {
  const q = new URLSearchParams(params).toString();
  const res = await fetch(`${BASE_URL}/v1/account/list?${q}`);
  return res.json();
}

export async function addAccount(body) {
  const res = await fetch(`${BASE_URL}/v1/account/add`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return res.json();
}

export async function uploadToPlatform(body) {
  const res = await fetch(`${BASE_URL}/v1/upload/to-platform`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return res.json();
}

export async function uploadToMultiple(body) {
  const res = await fetch(`${BASE_URL}/v1/upload/to-multiple`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return res.json();
}

export async function getDashboardStats(params = {}) {
  const q = new URLSearchParams(params).toString();
  const res = await fetch(`${BASE_URL}/v1/dashboard/stats?${q}`);
  return res.json();
}
