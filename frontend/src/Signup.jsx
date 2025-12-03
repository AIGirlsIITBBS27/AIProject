import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./Signup.css";
import { signupUser } from "./api";

function Signup() {
  const [formData, setFormData] = useState({
    name: "",
    dob: "",
    gender: "",
    country: "",
    email: "",
    phone: "",
  });

  const [generatedCreds, setGeneratedCreds] = useState(null);
  const navigate = useNavigate();

  const generateUsername = (email) => {
    if (!email.includes("@")) return email.toLowerCase();
    return email.split("@")[0].toLowerCase();
  };

  const generatePassword = (name, dob) => {
    const cleanName = name.replace(/[^a-zA-Z]/g, "").toLowerCase();
    const first3 = cleanName.slice(0, 3);
    const year = new Date(dob).getFullYear();
    return first3 + year;
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const username = generateUsername(formData.email);
    const password = generatePassword(formData.name, formData.dob);

     try {
    await signupUser({
      name: formData.name,
      dob: formData.dob,
      gender: formData.gender,
      country: formData.country,
      email: formData.email,
      phone: formData.phone,
      username: username,
      password: password,
    });

      setGeneratedCreds({ username, password });

    } catch (err) {
      alert(err.response?.data?.detail || "Signup failed");
    }
  };

  return (
    <div className="signup-page">
      <div className="signup-container">
        <form className="signup-form" onSubmit={handleSubmit}>
          <h2>Create Account</h2>

          <div className="form-group">
            <label>Name:</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
            />
          </div>

          {/* DOB field */}
          <div className="form-group">
            <label>Date of Birth:</label>
            <input
              type="date"
              name="dob"
              value={formData.dob}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Gender:</label>
            <select
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              required
            >
              <option value="">Select</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div className="form-group">
            <label>Country:</label>
            <input
              type="text"
              name="country"
              value={formData.country}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Email:</label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>Phone:</label>
            <input
              type="tel"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              required
            />
          </div>

          <button type="submit" className="btn-register">Register</button>

          <p className="already-user">
            Already a user? <Link to="/login">Login</Link>
          </p>
        </form>

        {/* Display generated username & password */}
        {generatedCreds && (
          <div
            style={{
              marginTop: "20px",
              padding: "15px",
              border: "1px solid #ccc",
              borderRadius: "8px",
            }}
          >
            <h3>Your Login Credentials</h3>
            <p><strong>Username:</strong> {generatedCreds.username}</p>
            <p><strong>Password:</strong> {generatedCreds.password}</p>

            <button onClick={() => navigate("/welcome")} style={{ marginTop: "10px" }}>
              Continue
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default Signup;
