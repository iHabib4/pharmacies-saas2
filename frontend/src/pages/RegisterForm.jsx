// pages/RegisterForm.jsx
import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

export default function RegisterForm() {
  const { role } = useParams(); // customer, pharmacy, supplier, rider
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Role:", role, "Name:", name, "Email:", email);
    alert(`Registered as ${role} with email ${email}`);
    // After registration, navigate to login
    navigate("/login");
  };

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h2>Register as {role.charAt(0).toUpperCase() + role.slice(1)}</h2>
      <form onSubmit={handleSubmit} style={{ display: "inline-block", textAlign: "left" }}>
        <div style={{ marginBottom: "10px" }}>
          <input
            type="text"
            placeholder="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            style={{ width: "200px", padding: "5px" }}
          />
        </div>
        <div style={{ marginBottom: "10px" }}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={{ width: "200px", padding: "5px" }}
          />
        </div>
        <div style={{ marginBottom: "10px" }}>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={{ width: "200px", padding: "5px" }}
          />
        </div>
        <button type="submit" style={{ width: "100%" }}>Register</button>
      </form>
    </div>
  );
}
