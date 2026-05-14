import axios from "axios";

const API_URL = "http://127.0.0.1:8080";

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (!error.response) {
      return Promise.reject(
        new Error("Brak połączenia z serwerem. Spróbuj ponownie później.")
      );
    }

    const { status, data } = error.response;

    const message =
      data?.message ||
      (typeof data === "string" && data) ||
      "Wystąpił błąd po stronie serwera";

    if (status === 401) {
      localStorage.removeItem("token");
    }

    const err = new Error(message);
    err.status = status;
    err.payload = data;

    return Promise.reject(err);
  }
);
