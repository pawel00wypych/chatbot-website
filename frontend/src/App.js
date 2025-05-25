import React, { useState, useEffect } from "react";
import Chat from "./components/Chat";
import "./App.css";


function App() {
  const [theme, setTheme] = useState("light");

  // Load saved theme or default to light
  useEffect(() => {
    const saved = localStorage.getItem("theme");
    if (saved === "dark" || saved === "light") {
      setTheme(saved);
    }
  }, []);

  // Save theme to localStorage
  useEffect(() => {
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme((t) => (t === "light" ? "dark" : "light"));
  };

  return (
    <div className={`app-wrapper ${theme}`}>
      <header>
        <h1>Chatbot</h1>
        <button onClick={toggleTheme} className="theme-toggle-btn">
          {theme === "light" ? "🌙 Dark Mode" : "☀️ Light Mode"}
        </button>
      </header>
      <Chat />
    </div>
  );
}

export default App;
