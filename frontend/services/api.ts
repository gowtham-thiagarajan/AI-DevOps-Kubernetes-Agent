import axios from "axios";

const baseURL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

const apiClient = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 300000, // 5 minute timeout for investigation
});

export async function fetchHealth() {
  const response = await apiClient.get("/health");
  return response.data;
}

export async function runInvestigation() {
  const response = await apiClient.post("/investigate");
  return response.data;
}

export async function fetchInvestigationHistory() {
  const response = await apiClient.get("/history");
  return response.data;
}

export async function fetchClusters() {
  const response = await apiClient.get("/clusters");
  return response.data;
}

export async function login(email: string, password: string) {
  const response = await apiClient.post("/api/auth/login", { email, password });
  return response.data;
}

export async function getCurrentUser() {
  const response = await apiClient.get("/api/auth/me");
  return response.data;
}

export async function logout() {
  const response = await apiClient.post("/api/auth/logout");
  return response.data;
}

export interface InvestigationResult {
  status: string;
  investigation: {
    pods: Record<string, unknown>;
    logs: Record<string, unknown>;
    events: Record<string, unknown>;
    deployments: Record<string, unknown>;
    network: Record<string, unknown>;
  };
  diagnosis?: {
    root_cause: string;
    explanation: string;
    fix: string;
    kubectl_command: string;
    prevention: string;
    confidence: number;
  };
}

