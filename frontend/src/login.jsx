import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";
 import { loginUser } from "./api";   // <-- add this


function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();



const handleLogin = async (e) => {
  e.preventDefault();

  try {
    const res = await loginUser({ username, password });
    alert("Login successful!");
    navigate("/chatbot");
  } catch (err) {
    alert(err.response?.data?.detail || "Invalid username or password");
  }
};



  return (
    <div className="login-page">
      <div className="login-container">
        <form className="login-form" onSubmit={handleLogin}>
          <h2>Login</h2>
          <div className="form-group">
            <label>Username:</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label>Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          
          <button type="submit">Login</button>

          <p className="forgot-password">
              <a href="/forgot-password">Forgot Password?</a>
          </p>

        </form>
      </div>
    </div>
  );
}

export default Login;
