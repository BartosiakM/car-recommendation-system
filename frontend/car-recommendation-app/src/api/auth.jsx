import { api } from "./client";

export async function login(username, password) {
  const response = await api.post("/auth/login", { username, password });
  return response.data; 
}

export async function register(username, password) {
  const response = await api.post("/auth/register", { username, password });
  return response.data;
}

export async function validateToken() {
  const response = await api.get("/auth/me");
  return response.data; 
}

export function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("id");
}
