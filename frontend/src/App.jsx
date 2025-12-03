import React, { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import "./App.css";
import Login from "./Login";
import Chatbot from "./chatbot";
import Signup from "./Signup";
import Welcome from "./Welcome";
import ForgotPassword from "./ForgotPassword";


function Home() {
  useEffect(() => {
    const videoUrls = [
      "/video/video1.mp4",
      "/video/video2.mp4",
      "/video/video3.mp4",
      "/video/video4.mp4",
      "/video/video5.mp4",
      "/video/video6.mp4",
      "/video/video7.mp4",
    ];

    const videoElement = document.getElementById("video-element");
    if (videoElement) {
      const randomVideo =
        videoUrls[Math.floor(Math.random() * videoUrls.length)];
      videoElement.src = randomVideo;
    }
  }, []);

  return (
    <div className="page">
      {/* Navbar */}
      <nav className="navbar">
        <div className="navdiv">
          <div className="logo">
            <Link to="/">MediCo</Link>
          </div>
          <ul>
            <li>
              <Link to="/login">Login</Link>
            </li>
            <li>
              <Link to="/signup">SignUp</Link>
            </li>
          </ul>
        </div>
      </nav>

      {/* Video Section */}
      <div id="background-video">
        <video id="video-element" autoPlay muted loop></video>
      </div>

      {/* About Section */}
      <section className="about-section">
        <h1 style={{ color: "black" }}>Your Health Assistant at Your Doorstep</h1>
        <p>
          We are a team of engineers dedicated to improving healthcare accessibility through intelligent technology.
          Our project introduces a multilingual health assistant chatbot that enables users to communicate their
          health concerns in their native language, ensuring clarity and comfort during conversations.
        </p>
        <p>
          The chatbot leverages AI-driven question–answering techniques and a knowledge graph to analyze symptoms,
          identify possible conditions, and provide appropriate guidance, explanations, and remedies. In cases where
          the system detects a potential medical emergency, it automatically notifies registered doctors, allowing
          them to take over the conversation and provide professional counseling in real time.
        </p>
        <p>
          Our mission is to create a secure, inclusive, and efficient online healthcare platform that bridges the gap
          between individuals and medical professionals, making quality health support accessible to everyone.
        </p>
      </section>

      {/* Contact Section */}
      <section className="contact-section">
        <h2>Contact Us</h2>
        <p>📞 Mobile: 9479XXXXXX</p>
        <p>✉️ Email: abc12XXXXXX@gmail.com</p>
      </section>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/Signup" element={<Signup />} />
        <Route path="/chatbot" element={<Chatbot />} />
        <Route path="/welcome" element={<Welcome />} />
      </Routes>
    </Router>
  );
}

export default App;
