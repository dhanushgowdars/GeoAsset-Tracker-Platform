import axios from "axios";

import { API_BASE_URL } from "../config/api";
import { getToken } from "../utils/storage";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000,
});

api.interceptors.request.use((config) => {
  const token = getToken();

  if (token) {
    // Ensure headers object exists and set Authorization header
    if (!config.headers) {
      config.headers = {};
    }
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

export default api;
