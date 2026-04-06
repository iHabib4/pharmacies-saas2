import React from "react";
import { Link } from "react-router-dom";

function LandingPage() {
  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Welcome to UW PICO SaaS</h1>
      <h2>Register</h2>
      <p>Choose your role:</p>
      <div>
        <Link to="/register/customer"><button>Customer</button></Link>{" "}
        <Link to="/register/pharmacy"><button>Pharmacy Owner</button></Link>{" "}
        <Link to="/register/rider"><button>Rider</button></Link>{" "}
        <Link to="/register/supplier"><button>Supplier</button></Link>
      </div>
      <h2>Already have an account?</h2>
      <Link to="/login"><button>Login</button></Link>
    </div>
  );
}

export default LandingPage;
