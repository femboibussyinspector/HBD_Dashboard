import axios from 'axios';

// 1. Define your Backend URL
// In production, VITE_API_URL should point to the API host (e.g. "https://dashboard.cityhangaround.com").
// In dev, we rely on Vite proxy at /api which rewrites to the local backend.
const apiBase = import.meta.env.DEV ? "/api" : (import.meta.env.VITE_API_URL || "");

// 2. Create the Axios Instance
const api = axios.create({
  baseURL: apiBase,
  headers: {
    "Content-Type": "application/json",
  },
});

// 3. Optional: Add a logger to help us debug later
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Connection Error:", error);
    return Promise.reject(error);
  }
);

export default api;