import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Register = () => {


  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = async () => {
    try {
      const passwordValid = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{10,}$/.test(password);

      if (!passwordValid) {
        alert("Password must be at least 10 characters long and include:\n- 1 uppercase letter\n- 1 lowercase letter\n- 1 digit\n- 1 special character");
        return;
      }

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
        <p>Already have an account?</p>
        <button onClick={() => navigate("/login")} className="link-btn">Login</button>
      </div>
    </div>
  );
};

export default Register;
