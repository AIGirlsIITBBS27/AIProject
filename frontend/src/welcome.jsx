import React, { useEffect } from "react"
import "./Welcome.css"

function Welcome() {
  useEffect(() => {
    const card = document.querySelector(".welcome-card")
    card.style.opacity = "0"
    card.style.transform = "translateY(20px)"
    setTimeout(() => {
      card.style.transition = "all 0.8s ease"
      card.style.opacity = "1"
      card.style.transform = "translateY(0)"
    }, 100)
  }, [])

  return (
    <div className="welcome-page">
      <div className="welcome-card">
        <h1 className="welcome-title">
          Welcome to <span>MediCo</span>!
        </h1>
        <p className="welcome-text">Your registration was successful 🎉</p>
        <p className="welcome-text">
          You can now explore the chatbot or log in anytime.
        </p>
        <a href="/login" className="welcome-btn">Go to Login</a>
      </div>
      <div className="welcome-glow"></div>
    </div>
  )
}

export default Welcome
