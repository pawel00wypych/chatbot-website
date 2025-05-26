import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = ({ setUser }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const login = async () => {
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();
    if (res.ok) {
      localStorage.setItem("token", data.access);
      localStorage.setItem("user", JSON.stringify({ email: data.email }));
      setUser({ email: data.email });
      navigate("/");
    } else {
      alert(data.error);
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-form">
        <h2>Login</h2>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          className="input-field"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          className="input-field"
        />
        <button onClick={login} className="login-btn">
          Login
        </button>
        <p>Don't have an account?</p>
        <button onClick={() => navigate("/register")} className="link-btn">
          Register
        </button>
      </div>
    </div>
  );
};

export default Login;
