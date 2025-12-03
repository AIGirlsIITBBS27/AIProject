import React, { useState } from "react";
import { forgotPassword } from "./api";
import "./Login.css";

function ForgotPassword() {
  const [name, setName] = useState("");
  const [dob, setDob] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await forgotPassword({ name, dob });
      setResult(res.data);
    } catch (err) {
      alert(err.response?.data?.detail || "User not found");
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <form className="login-form" onSubmit={handleSubmit}>
          <h2>Recover Password</h2>

          <div className="form-group">
            <label>Full Name:</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label>Date of Birth:</label>
            <input
              type="date"
              value={dob}
              onChange={(e) => setDob(e.target.value)}
              required
            />
          </div>

          <button type="submit">Recover</button>

          {result && (
            <div className="result-box">
              <h3>Your Login Details</h3>
              <p><strong>Username:</strong> {result.username}</p>
              <p><strong>Password:</strong> {result.password}</p>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}

export default ForgotPassword;
