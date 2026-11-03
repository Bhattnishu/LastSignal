
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
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [message, setMessage] = useState("");
  const [contactMethod, setContactMethod] = useState("PHONE");
  const [contactValue, setContactValue] = useState("");
  const [sending, setSending] = useState(false);
  const [successId, setSuccessId] = useState(null);

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

  async function handleRecoveryRequest(event) {
    event.preventDefault();

    if (!selectedMatch || !message.trim() || !contactValue.trim()) {
      setError("Please fill in all fields.");
      return;
    }

    setSending(true);
    setError("");

    try {
      await apiRequest("/items/recovery-requests/", {
        method: "POST",
        body: JSON.stringify({
          lost_report: Number(id),
          found_report: selectedMatch.report.id,
          message: message.trim(),
          contact_method: contactMethod,
          contact_value: contactValue.trim(),
        }),
      });

      setSuccessId(selectedMatch.report.id);
      setSelectedMatch(null);
      setMessage("");
      setContactValue("");
    } catch (err) {
      setError(err.message);
    } finally {
      setSending(false);
    }
  }

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

              {successId === match.report.id ? (
                <p className="recovery-success">
                  Your message and contact details have been sent!
                </p>
              ) : (
                <button
                  className="recovery-request-btn"
                  onClick={() => {
                    setSelectedMatch(match);
                    setMessage("");
                    setContactValue("");
                    setContactMethod("PHONE");
                    setError("");
                  }}
                >
                  Contact Finder
                </button>
              )}
            </div>
          ))}

          <Link to={`/investigation/${id}`} className="investigation-link">
            Start an Investigation →
          </Link>
        </div>
      </main>

      {selectedMatch && (
        <div className="recovery-modal-overlay">
          <div className="recovery-modal">
            <h2>Contact Finder</h2>

            <p>
              Explain why you believe this {selectedMatch.report.item_name}
               belongs to you and share your contact details.
            </p>

            <form onSubmit={handleRecoveryRequest}>
              <textarea
                value={message}
                onChange={(event) => setMessage(event.target.value)}
                placeholder="Explain why this item belongs to you..."
                rows={4}
                required
              />

              <select
                value={contactMethod}
                onChange={(event) => setContactMethod(event.target.value)}
              >
                <option value="PHONE">Phone Number</option>
                <option value="EMAIL">Email Address</option>
              </select>

              <input
                type={contactMethod === "EMAIL" ? "email" : "tel"}
                value={contactValue}
                onChange={(event) => setContactValue(event.target.value)}
                placeholder={
                  contactMethod === "EMAIL"
                    ? "Your email address"
                    : "Your phone number"
                }
                required
              />

              {error && <p className="form-error">{error}</p>}

              <div className="recovery-modal-actions">
                <button
                  type="button"
                  className="recovery-cancel-btn"
                  onClick={() => {
                    setSelectedMatch(null);
                    setError("");
                  }}
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="recovery-request-btn"
                  disabled={sending || !message.trim() || !contactValue.trim()}
                >
                  {sending ? "Sending..." : "Send Details"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <Footer />
    </>
  );
}

export default LostResults;
