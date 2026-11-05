import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

import Navbar from "../components/Navbar/Navbar";
import Footer from "../components/Footer/Footer";

import MatchCard from "../components/LostResults/MatchCard";
import RecoveryRequestModal from "../components/LostResults/RecoveryRequestModal";

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
  const [sentRequests, setSentRequests] = useState({});

  useEffect(() => {
    async function fetchData() {
      try {
        const matchData = await apiRequest(
          `/items/my-reports/${id}/matches/`
        );

        setResults(matchData);

        const requestData = await apiRequest(
          "/items/recovery-requests/sent/"
        );

        const requests = Array.isArray(requestData)
          ? requestData
          : requestData.results || [];

        const requestMap = {};

        requests.forEach((request) => {
          if (Number(request.lost_report) === Number(id)) {
            requestMap[request.found_report] = request.status;
          }
        });

        setSentRequests(requestMap);

        try {
          const notificationData = await apiRequest(
            "/items/notifications/"
          );

          const notifications = Array.isArray(notificationData)
            ? notificationData
            : notificationData.results || [];

          const unreadMatches = notifications.filter(
            (notification) =>
              !notification.is_read &&
              notification.title === "Possible match found!" &&
              Number(notification.lost_report_id) === Number(id)
          );

          await Promise.all(
            unreadMatches.map((notification) =>
              apiRequest(
                `/items/notifications/${notification.id}/read/`,
                { method: "PATCH" }
              )
            )
          );

          if (unreadMatches.length > 0) {
            window.dispatchEvent(
              new Event("notifications-updated")
            );
          }
        } catch (notificationError) {
          console.error("Could not update notifications:", notificationError);
        }
      } catch (err) {
        setError(err.message);
      }
    }

    fetchData();
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
      const response = await apiRequest(
        "/items/recovery-requests/",
        {
          method: "POST",
          body: JSON.stringify({
            lost_report: Number(id),
            found_report: selectedMatch.report.id,
            message: message.trim(),
            contact_method: contactMethod,
            contact_value: contactValue.trim(),
          }),
        }
      );

      setSentRequests((previous) => ({
        ...previous,
        [selectedMatch.report.id]: response.status || "PENDING",
      }));

      setSelectedMatch(null);
      setMessage("");
      setContactValue("");
    } catch (err) {
      setError(err.message);
    } finally {
      setSending(false);
    }
  }

  function getRequestLabel(status) {
    if (status === "ACCEPTED") return "Request Accepted";
    if (status === "REJECTED") return "Request Rejected";
    if (status === "COMPLETED") return "Recovery Completed";
    return "Request Sent";
  }

  function openContactModal(match) {
    setSelectedMatch(match);
    setMessage("");
    setContactValue("");
    setContactMethod("PHONE");
    setError("");
  }

  function closeContactModal() {
    setSelectedMatch(null);
    setError("");
  }

  return (
    <>
      <Navbar />

      <main className="lost-results-page">
        <div className="lost-results-container">
          <Link to="/" className="back-link">
            ← Back to Home
          </Link>

          <h1>Lost Item Search Results</h1>
          <p>Here are the possible matches we found for your report.</p>

          {error && !selectedMatch && (
            <p className="form-error">{error}</p>
          )}

          {!results && !error && (
            <p>Searching for possible matches...</p>
          )}

          {results && results.total_matches === 0 && (
            <p className="no-matches">
              No possible matches found right now. Your report remains
              active, so we'll be able to find future matches.
            </p>
          )}

          <div className="matches-list">
            {results?.matches?.map((match) => (
              <MatchCard
                key={match.report.id}
                match={match}
                requestStatus={sentRequests[match.report.id]}
                getRequestLabel={getRequestLabel}
                onContact={openContactModal}
              />
            ))}
          </div>

          <Link
            to={`/investigation/${id}`}
            className="investigation-link"
          >
            Start an Investigation →
          </Link>
        </div>
      </main>

      <RecoveryRequestModal
        selectedMatch={selectedMatch}
        message={message}
        setMessage={setMessage}
        contactMethod={contactMethod}
        setContactMethod={setContactMethod}
        contactValue={contactValue}
        setContactValue={setContactValue}
        sending={sending}
        error={error}
        onClose={closeContactModal}
        onSubmit={handleRecoveryRequest}
      />

      <Footer />
    </>
  );
}

export default LostResults;