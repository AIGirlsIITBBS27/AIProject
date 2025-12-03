import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./Chatbot.css";
import { FaRobot, FaUserCircle } from "react-icons/fa";
import { askQuestion } from "./api";

function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [expanded, setExpanded] = useState(false);

  const handleSend = async () => {
    if (input.trim() === "") return;

    const newMessages = [
      ...messages,
      { sender: "user", text: input },
      { sender: "bot", text: "Thinking...", triage_questions: [] },
    ];

    setMessages(newMessages);
    setInput("");
    setExpanded(true);

    try {
      const res = await askQuestion(input);

      const botReply = res.data.answer || "Sorry, I couldn't understand.";
      const triageQuestions = res.data.triage_questions || [];

      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          sender: "bot",
          text: botReply,
          triage_questions: triageQuestions,
        };
        return updated;
      });
    } catch (err) {
      console.error("Backend error:", err);
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          sender: "bot",
          text: "Server error, please try again later.",
          triage_questions: [],
        };
        return updated;
      });
    }
  };

  return (
    <div className="chatbot-page">
      {/* Navbar */}
      <nav className="chatbot-navbar">
        <div className="logo">
          <Link to="/">MediCo</Link>
        </div>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>

          <li>
            <Link to="/login">Logout</Link>
          </li>
        </ul>
      </nav>

      {/* Chatbot Container */}
      <div className="chatbot-container">
        <h2 className="chatbot-header">💬 Ask Your Health Assistant</h2>

        <div className={`chat-window ${expanded ? "expanded" : ""}`}>
          {messages.length === 0 ? (
            <p className="placeholder-text">Start by asking a health question...</p>
          ) : (
            messages.map((msg, i) => (
              <div key={i} className={`message ${msg.sender}`}>
                {msg.sender === "bot" && (
                  <FaRobot className="icon bot-icon" size={24} />
                )}
                {msg.sender === "user" && (
                  <FaUserCircle className="icon user-icon" size={24} />
                )}

                <div className="message-text">
                  {msg.text}

                  {/* ---------- SHOW TRIAGE QUESTIONS ---------- */}
                  {msg.triage_questions &&
                    msg.triage_questions.length > 0 && (
                      <div className="triage-list">
                        {msg.triage_questions.map((q, idx) => (
                          <p key={idx} className="triage-question">
                            👉 {q}
                          </p>
                        ))}
                      </div>
                    )}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Input Box */}
        <div className="chat-input-area">
          <input
            type="text"
            placeholder="Type your question..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default Chatbot;
