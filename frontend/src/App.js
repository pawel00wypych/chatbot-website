import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Chat from "./components/Chat";
import Login from "./components/Login";
import Register from "./components/Register";
import './App.css';

function App() {
  const [theme, setTheme] = useState("light");
  const [user, setUser] = useState(() => {
            const savedUser = localStorage.getItem("user");
            console.log("savedUser:", savedUser);
            return savedUser ? JSON.parse(savedUser) : null;
          });

  console.log("USER STATE:", user);


  useEffect(() => {
    const saved = localStorage.getItem("theme");
    if (saved) setTheme(saved);
  }, []);

  useEffect(() => {
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((t) => (t === "light" ? "dark" : "light"));
  };

  return (
    <Router>
      <div className={`app-wrapper ${theme}`}>
        <header>
          <h1>Chatbot</h1>
          <button onClick={toggleTheme} className="theme-toggle-btn">
            {theme === "light" ? "🌙 Dark Mode" : "☀️ Light Mode"}
          </button>
        </header>

        <Routes>
          <Route
            path="/"
            element={
              user ? <Chat /> : <Navigate to="/login" />
            }
          />
          <Route path="/login" element={<Login setUser={setUser} />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
