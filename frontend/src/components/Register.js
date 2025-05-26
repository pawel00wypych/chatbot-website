import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Register = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      const res = await fetch("/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();
      if (res.ok) {
        alert("Registered! Please login.");
        navigate("/login");
      } else {
        alert(data.error || "Registration failed");
      }
    } catch (err) {
      alert("Error registering");
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-form">
        <h2>Register</h2>
        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
        <button onClick={handleRegister} className="theme-toggle-btn">Register</button>
      </div>
    </div>
  );
};

export default Register;
