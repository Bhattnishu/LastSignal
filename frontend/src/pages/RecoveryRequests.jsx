
import { useEffect, useState } from "react";
import { apiRequest } from "../services/api";
import "./RecoveryRequests.css";

function RecoveryRequests() {
  const [received, setReceived] = useState([]);
  const [sent, setSent] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadRequests() {
      try {
        const [r, s] = await Promise.all([
          apiRequest("/items/recovery-requests/received/"),
          apiRequest("/items/recovery-requests/sent/"),
        ]);

        setReceived(Array.isArray(r) ? r : r.results || []);
        setSent(Array.isArray(s) ? s : s.results || []);
      } catch (err) {
        setError(err.message);
      }
    }

    loadRequests();
  }, []);

  return (
    <section className="activity-section recovery-requests">
      <h2>Received Recovery Messages</h2>

      {error && <p className="form-error">{error}</p>}

      {received.length === 0 && (
        <p>No recovery messages received yet.</p>
      )}

      {received.map((r) => (
        <article className="activity-card" key={r.id}>
          <h3>{r.found_item_name}</h3>
          <p>From: {r.requester_name}</p>
          <p>Lost item: {r.lost_item_name}</p>

          <p><strong>Message:</strong> {r.message}</p>

          <p>
            <strong>Contact method:</strong> {r.contact_method}
          </p>

          <p>
            <strong>Contact details:</strong> {r.contact_value}
          </p>

          <p>You can now contact this person directly.</p>
        </article>
      ))}

      <h2>Sent Recovery Messages</h2>

      {sent.length === 0 && (
        <p>You haven't sent any recovery messages yet.</p>
      )}

      {sent.map((r) => (
        <article className="activity-card" key={r.id}>
          <h3>{r.lost_item_name}</h3>
          <p>Found item: {r.found_item_name}</p>
          <p>Your message: {r.message}</p>
          <p>Contact details shared: {r.contact_value}</p>
          <p>Message sent successfully.</p>
        </article>
      ))}
    </section>
  );
}

export default RecoveryRequests;
