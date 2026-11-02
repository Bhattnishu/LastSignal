import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import Navbar from "../components/Navbar/Navbar";
import Footer from "../components/Footer/Footer";
import { apiRequest } from "../services/api";
import "./LostResults.css";

function LostResults() {
  const { id } = useParams();
  const [results, setResults] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchMatches() {
      try {
        const data = await apiRequest(`/items/my-reports/${id}/matches/`);
        setResults(data);
      } catch (err) {
        setError(err.message);
      }
    }

    fetchMatches();
  }, [id]);

  return (
    <>
      <Navbar />

      <main className="lost-results-page">
        <div className="lost-results-container">
          <Link to="/" className="back-link">← Back to Home</Link>

          <h1>Lost Item Search Results</h1>
          <p>Here are the possible matches we found for your report.</p>

          {error && <p className="form-error">{error}</p>}

          {!results && !error && <p>Searching for possible matches...</p>}

          {results && results.total_matches === 0 && (
            <p className="no-matches">
              No possible matches found right now. Your report remains active,
              so we'll be able to find future matches.
            </p>
          )}

          {results?.matches?.map((match) => (
            <div className="match-card" key={match.report.id}>
              <h2>{match.report.item_name}</h2>
              <p>Category: {match.report.category}</p>
              <p>Brand: {match.report.brand || "Not specified"}</p>
              <p>Color: {match.report.color || "Not specified"}</p>
              <p>Location: {match.report.location}, {match.report.city}</p>
              <p>Match score: {match.match_score}</p>

              <p>Why it may match:</p>
              <ul>
                {match.match_reasons.map((reason, index) => (
                  <li key={index}>{reason}</li>
                ))}
              </ul>
            </div>
          ))}

          <Link to={`/investigation/${id}`} className="investigation-link">
            Start an Investigation →
          </Link>
        </div>
      </main>

      <Footer />
    </>
  );
}

export default LostResults;