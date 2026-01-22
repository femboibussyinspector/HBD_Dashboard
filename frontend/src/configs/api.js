import axios from 'axios';

// 1. Define your Backend URL
// If your Python terminal says "Running on http://127.0.0.1:5000", keep this.
// If it says port 8000, change it to 8000.
const API_BASE_URL = "http://127.0.0.1:5000";

// 2. Create the Axios Instance
const api = axios.create({
  baseURL: API_BASE_URL,
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