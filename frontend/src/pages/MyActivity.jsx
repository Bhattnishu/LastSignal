
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar/Navbar";
import Footer from "../components/Footer/Footer";
import { apiRequest } from "../services/api";
import "./MyActivity.css";

function MyActivity() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

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

  return (
    <>
      <Navbar />

      <main className="my-activity-page">
        <div className="my-activity-container">
          <Link to="/" className="back-link">
            ← Back to Home
          </Link>

          <h1>My Activity</h1>
          <p>Keep track of the items you have reported.</p>

          {loading && <p>Loading your reports...</p>}

          {error && <p className="form-error">{error}</p>}

          {!loading && !error && reports.length === 0 && (
            <div className="activity-empty">
              <h2>No activity yet</h2>
              <p>Your lost and found reports will appear here.</p>
            </div>
          )}

          <div className="activity-list">
            {reports.map((report) => (
              <article className="activity-card" key={report.id}>
                <div className="activity-card-header">
                  <span
                    className={`report-type ${report.report_type.toLowerCase()}`}
                  >
                    {report.report_type === "LOST" ? "Lost Item" : "Found Item"}
                  </span>

                  <span className="report-status">
                    {report.status}
                  </span>
                </div>

                <h2>{report.item_name}</h2>

                <p>Category: {report.category}</p>
                <p>Location: {report.location}, {report.city}</p>

                <small>
                  Submitted: {new Date(report.created_at).toLocaleDateString()}
                </small>
              </article>
            ))}
          </div>
        </div>
      </main>

      <Footer />
    </>
  );
}

export default MyActivity;
