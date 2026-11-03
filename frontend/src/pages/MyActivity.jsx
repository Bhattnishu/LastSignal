
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar/Navbar";
import Footer from "../components/Footer/Footer";
import { apiRequest } from "../services/api";
import RecoveryRequests from "./RecoveryRequests";
import "./MyActivity.css";

function MyActivity() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [deletingId, setDeletingId] = useState(null);

  useEffect(() => {
    async function fetchReports() {
      try {
        const data = await apiRequest("/items/my-reports/");
        setReports(Array.isArray(data) ? data : data.results || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchReports();
  }, []);

  async function handleDelete(report) {
    const confirmed = window.confirm(
      `Are you sure you want to permanently delete your ${report.report_type.toLowerCase()} report for "${report.item_name}"?`
    );

    if (!confirmed) return;

    setDeletingId(report.id);
    setError("");

    try {
      await apiRequest(`/items/my-reports/${report.id}/`, {
        method: "DELETE",
      });

      setReports((previous) =>
        previous.filter((item) => item.id !== report.id)
      );
    } catch (err) {
      setError(err.message);
    } finally {
      setDeletingId(null);
    }
  }

  return (
    <>
      <Navbar />

      <main className="my-activity-page">
        <div className="my-activity-container">
          <Link to="/" className="back-link">
            ← Back to Home
          </Link>

          <h1>My Activity</h1>
          <p>Keep track of your reports and recovery requests.</p>

          {error && <p className="form-error">{error}</p>}

          {loading ? (
            <p>Loading your reports...</p>
          ) : (
            <>
              <section className="activity-section">
                <h2>My Reports</h2>

                {reports.length === 0 ? (
                  <div className="activity-empty">
                    <p>You haven't submitted any reports yet.</p>
                  </div>
                ) : (
                  <div className="activity-list">
                    {reports.map((report) => (
                      <article
                        className="activity-card"
                        key={report.id}
                      >
                        <div className="activity-card-header">
                          <span
                            className={`report-type ${report.report_type.toLowerCase()}`}
                          >
                            {report.report_type === "LOST"
                              ? "Lost Item"
                              : "Found Item"}
                          </span>

                          <span className="report-status">
                            {report.status}
                          </span>
                        </div>

                        <h2>{report.item_name}</h2>

                        <p>Category: {report.category}</p>
                        <p>
                          Location: {report.location}, {report.city}
                        </p>

                        <small>
                          Submitted:{" "}
                          {new Date(
                            report.created_at
                          ).toLocaleDateString()}
                        </small>

                        <div className="activity-card-actions">
                          <button
                            className="delete-report-btn"
                            onClick={() => handleDelete(report)}
                            disabled={deletingId === report.id}
                            title="Delete report"
                          >
                            🗑️{" "}
                            {deletingId === report.id
                              ? "Deleting..."
                              : "Delete"}
                          </button>
                        </div>
                      </article>
                    ))}
                  </div>
                )}
              </section>

              <RecoveryRequests />
            </>
          )}
        </div>
      </main>

      <Footer />
    </>
  );
}

export default MyActivity;
