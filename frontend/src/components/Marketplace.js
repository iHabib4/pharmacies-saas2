import React, { useState } from "react";

function Marketplace() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const searchMedicine = async () => {
    try {
      const res = await fetch(
        `http://localhost:8000/api/products/search/?q=${query}`
      );
      if (!res.ok) throw new Error("Network response was not ok");
      const data = await res.json();
      setResults(data);
    } catch (error) {
      console.error("Fetch error:", error);
      alert("Failed to fetch medicines. Check server or CORS settings.");
    }
  };

  return (
    <div>
      <h2>Search Medicines</h2>

      <input
        type="text"
        placeholder="Enter medicine name"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyPress={(e) => e.key === "Enter" && searchMedicine()}
      />

      <button onClick={searchMedicine}>Search</button>

      <hr />

      <h3>Results:</h3>

      {results.map((item, index) => (
        <div
          key={index}
          style={{ border: "1px solid #ccc", margin: "10px", padding: "10px" }}
        >
          <p><strong>{item.name}</strong></p>
          <p>Pharmacy: {item.pharmacy}</p>
          <p>Price: ${item.price}</p>
          <p>Stock: {item.stock}</p>
        </div>
      ))}
    </div>
  );
}

export default Marketplace;
