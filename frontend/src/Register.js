import React, { useState } from "react";

function Register() {
  const [form, setForm] = useState({
    email: "",
    password: "",
    pharmacy_name: "",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://127.0.0.1:8000/api/register/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      if (!res.ok) {
        const errorData = await res.json();
        alert("Error: " + JSON.stringify(errorData));
        return;
      }

      const data = await res.json();
      console.log(data);
      alert("Registration successful! Check console for details.");
    } catch (err) {
      console.error(err);
      alert("Network error. Make sure Django backend is running at 127.0.0.1:8000");
    }
  };

  return (
    <div>
      <h2>Register Pharmacy Owner</h2>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Email"
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <br />
        <input
          placeholder="Password"
          type="password"
          value={form.password}
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />
        <br />
        <input
          placeholder="Pharmacy Name"
          value={form.pharmacy_name}
          onChange={(e) => setForm({ ...form, pharmacy_name: e.target.value })}
        />
        <br />
        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default Register;
