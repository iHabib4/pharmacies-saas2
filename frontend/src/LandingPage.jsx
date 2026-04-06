// LandingPage.jsx
import React from "react";
import { useNavigate } from "react-router-dom";

export default function LandingPage() {
  const navigate = useNavigate();

  const handleRegister = (role) => {
    navigate(`/register/${role}`);
  };

  const handleLogin = () => {
    navigate("/login");
  };

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h1>Welcome to UW PICO</h1>
      <p>Please choose an option:</p>

      <div style={{ margin: "20px" }}>
        <button onClick={() => handleRegister("customer")} style={{ margin: "5px" }}>
          Register as Customer
        </button>
        <button onClick={() => handleRegister("pharmacy")} style={{ margin: "5px" }}>
          Register as Pharmacy Owner
        </button>
        <button onClick={() => handleRegister("supplier")} style={{ margin: "5px" }}>
          Register as Supplier
        </button>
        <button onClick={() => handleRegister("rider")} style={{ margin: "5px" }}>
          Register as Rider
        </button>
      </div>

      <div style={{ marginTop: "40px" }}>
        <button onClick={handleLogin}>Login</button>
      </div>
    </div>
  );
}
