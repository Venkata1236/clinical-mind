import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 120000, // 2 min — crew takes time
});

export const checkEligibility = (patientData) =>
  api.post("/api/v1/check-eligibility", patientData);

export const getHistory = () =>
  api.get("/api/v1/history");

export default api;