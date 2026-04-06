import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate, useParams } from "react-router-dom";

// Dashboards
import PharmacyDashboard from "./pages/PharmacyDashboard";
import RiderDashboard from "./pages/RiderDashboard";
import SupplierDashboard from "./pages/SupplierDashboard";
import CustomerDashboard from "./pages/CustomerDashboard";

// ---------- App Component ----------
export default function App() {
  // Track logged-in role to redirect to dashboard
  const [loggedInRole, setLoggedInRole] = useState("");

  // If logged in, show the dashboard
  if (loggedInRole === "customer") return <CustomerDashboard />;
  if (loggedInRole === "pharmacy") return <PharmacyDashboard />;
  if (loggedInRole === "supplier") return <SupplierDashboard />;
  if (loggedInRole === "rider") return <RiderDashboard />;

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage onLogin={setLoggedInRole} />} />
        <Route path="/register/:role" element={<RegisterPage />} />
      </Routes>
    </Router>
  );
}

// ---------- LandingPage Component ----------
function LandingPage() {
  const navigate = useNavigate();

  const handleRegisterClick = (role) => {
    navigate(`/register/${role}`);
  };

  const handleLoginClick = () => {
    navigate("/login");
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Welcome to UW PICO</h1>
      <p>Please choose an option:</p>

      <div style={{ margin: "20px" }}>
        <button onClick={() => handleRegisterClick("customer")} style={{ margin: "5px" }}>
          Register as Customer
        </button>
        <button onClick={() => handleRegisterClick("pharmacy")} style={{ margin: "5px" }}>
          Register as Pharmacy Owner
        </button>
        <button onClick={() => handleRegisterClick("supplier")} style={{ margin: "5px" }}>
          Register as Supplier
        </button>
        <button onClick={() => handleRegisterClick("rider")} style={{ margin: "5px" }}>
          Register as Rider
        </button>
      </div>

      <div style={{ marginTop: "20px" }}>
        <button onClick={handleLoginClick}>Login</button>
      </div>
    </div>
  );
}

// ---------- LoginPage Component ----------
function LoginPage({ onLogin }) {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    // For demo: determine role from email
    let role = "customer";
    if (email.includes("pharmacy")) role = "pharmacy";
    else if (email.includes("supplier")) role = "supplier";
    else if (email.includes("rider")) role = "rider";

    alert(`Logged in as ${email}`);
    onLogin(role); // redirect to dashboard
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit} style={{ display: "inline-block", textAlign: "left" }}>
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
        <button type="submit" style={{ width: "100%" }}>Login</button>
      </form>
      <div style={{ marginTop: "10px" }}>
        <button onClick={() => navigate("/")}>Back</button>
      </div>
    </div>
  );
}

// ---------- RegisterPage Component ----------
function RegisterPage() {
  const navigate = useNavigate();
  const { role } = useParams(); // customer, pharmacy, supplier, rider

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    alert(`Registered as ${role} with email ${email}`);
    navigate("/login");
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
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
      <div style={{ marginTop: "10px" }}>
        <button onClick={() => navigate("/")}>Back</button>
      </div>
    </div>
  );
}
