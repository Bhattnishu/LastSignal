const API_BASE_URL = (
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"
) + "/api";

async function refreshAccessToken() {
  const refreshToken = localStorage.getItem("refresh_token");

  if (!refreshToken) {
    return null;
  }

  const response = await fetch(`${API_BASE_URL}/auth/refresh/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      refresh: refreshToken,
    }),
  });

  if (!response.ok) {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    return null;
  }

  const data = await response.json();

  localStorage.setItem("access_token", data.access);

  if (data.refresh) {
    localStorage.setItem("refresh_token", data.refresh);
  }

  return data.access;
}

export async function apiRequest(endpoint, options = {}) {
  async function makeRequest(token) {
    const headers = {
      ...options.headers,
    };

    if (!(options.body instanceof FormData)) {
      headers["Content-Type"] = "application/json";
    }

    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    return fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });
  }

  let token = localStorage.getItem("access_token");
  let response = await makeRequest(token);

  if (response.status === 401 && token) {
    token = await refreshAccessToken();

    if (token) {
      response = await makeRequest(token);
    }
  }

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(
      data?.detail || JSON.stringify(data) || "Something went wrong"
    );
  }

  return data;
}
