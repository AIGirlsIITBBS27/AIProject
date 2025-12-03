import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// Chatbot
export const askQuestion = (question) =>
  API.post("/ask", { question });

// Signup
export const signupUser = (data) =>
  API.post("/auth/signup", data);

// Login
export const loginUser = (data) =>
  API.post("/auth/login", data);

export const forgotPassword = (data) =>
  API.post("/auth/forgot-password", data);
