// src/components/Register.js
import React, { useState } from "react";

const Register = () => {
  const [form, setForm] = useState({
    email: "",
    password: "",
    pharmacy_name: "",
  });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  // Update form state on input change
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // Submit form
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent page reload
    setMessage("");
    setError("");

    // Basic frontend validation
    if (!form.email || !form.password || !form.pharmacy_name) {
      setError("Please fill in all fields.");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:8000/api/register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      const data = await res.json();

      if (res.ok) {
        setMessage(`Registration successful! User ID: ${data.user_id}`);
        setForm({ email: "", password: "", pharmacy_name: "" }); // clear form
      } else {
        setError(data.error || "Something went wrong.");
      }
    } catch (err) {
      setError("Network error. Make sure Django backend is running at 127.0.0.1:8000");
      console.error(err);
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "auto", padding: "20px" }}>
      <h2>Register Pharmacy</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            name="email"
            value={form.email}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            name="password"
            value={form.password}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Pharmacy Name:</label>
          <input
            type="text"
            name="pharmacy_name"
            value={form.pharmacy_name}
            onChange={handleChange}
            required
          />
        </div>
        <button type="submit" style={{ marginTop: "10px" }}>Register</button>
      </form>

      {message && <p style={{ color: "green", marginTop: "10px" }}>{message}</p>}
      {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}
    </div>
  );
};

export default Register;
