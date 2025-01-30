import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState("");
  const [endpoint, setEndpoint] = useState("interactive-query");

  const executeQuery = async () => {
    try {
      setError("");
      const response = await axios.post(`http://127.0.0.1:8000/${endpoint}`, { query: query });
      setResults(response.data.rows || []);
    } catch (err) {
      setError(err.response?.data?.detail || "An error occurred while executing the query.");
    }
  };

  return (
    <div>
      <h1>Interactive Query Interface</h1>
      <select onChange={(e) => setEndpoint(e.target.value)}>
        <option value="interactive-query">Reddit</option>
        <option value="4chan-interactive-query">4chan</option>
      </select>
      <textarea
        rows="5"
        cols="50"
        placeholder="Write your SQL query here"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <br />
      <button onClick={executeQuery}>Execute Query</button>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <h2>Results</h2>
      {Array.isArray(results) && results.length > 0 ? (
        <table border="1">
          <thead>
            <tr>
              {Object.keys(results[0]).map((key) => (
                <th key={key}>{key}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {results.map((row, index) => (
              <tr key={index}>
                {Object.values(row).map((value, i) => (
                  <td key={i}>
                    {typeof value === "object" && value !== null ? JSON.stringify(value) : value}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No results to display</p>
      )}
    </div>
  );
}

export default App;
