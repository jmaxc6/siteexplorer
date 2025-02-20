import React, { useState } from "react";
import axios from "axios";

function App() {
  const [url, setUrl] = useState("");
  const [isScraping, setIsScraping] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  // Handle URL input change
  const handleUrlChange = (event) => {
    setUrl(event.target.value);
  };

  // Start the scraping process
  const startScraping = async () => {
    if (!url) {
      setErrorMessage("Please enter a valid URL.");
      return;
    }
    setIsScraping(true);
    setErrorMessage("");

    try {
      // Make a POST request to the backend to start scraping
      const response = await axios.post("http://localhost:5001/scrape", { url });

      // Process response if needed (e.g., show success message, etc.)
      console.log("Scraping completed:", response.data);
      alert("Scraping completed successfully!");
    } catch (error) {
      setErrorMessage("Error scraping the site. Please try again.");
      console.error("Error:", error);
    } finally {
      setIsScraping(false);
    }
  };

  return (
    <div className="App">
      <h1>Site Scraper</h1>
      <input
        type="text"
        value={url}
        onChange={handleUrlChange}
        placeholder="Enter site URL"
        style={{ width: "300px", padding: "10px" }}
      />
      <button onClick={startScraping} disabled={isScraping} style={{ padding: "10px", marginLeft: "10px" }}>
        {isScraping ? "Scraping..." : "Start Scraping"}
      </button>

      {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
    </div>
  );
}

export default App;
