
import { useParams, Link } from "react-router-dom";
import Navbar from "../components/Navbar/Navbar";
import Footer from "../components/Footer/Footer";
import TimelineForm from "../components/Investigation/TimelineForm";
import TimelineList from "../components/Investigation/TimelineList";
import AIAnalysis from "../components/Investigation/AIAnalysis";

import "./Investigation.css";
import { useEffect, useState } from "react";
import { apiRequest } from "../services/api";

function Investigation() {
  const { id } = useParams();

  const [investigationId, setInvestigationId] = useState(null);
  const [place, setPlace] = useState("");
  const [analysisSource, setAnalysisSource] = useState("");
  const [description, setDescription] = useState("");
  const [visitedAt, setVisitedAt] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);
  const [timelineEntries, setTimelineEntries] = useState([]);
  const [analysis, setAnalysis] = useState("");
  const [analysisLoading, setAnalysisLoading] = useState(false);

  useEffect(() => {
    async function loadInvestigation() {
      try {
        const data = await apiRequest("/investigations/", {
          method: "POST",
          body: JSON.stringify({ lost_report: Number(id) }),
        });

        setInvestigationId(data.id);
        setError("");
      } catch (err) {
        setError(err.message);
      }
    }

    loadInvestigation();
  }, [id]);

  useEffect(() => {
    if (!investigationId) return;

    async function fetchTimeline() {
      try {
        const data = await apiRequest("/investigations/my-timeline/");

        setTimelineEntries(
          data.filter(
            (entry) => Number(entry.investigation) === investigationId
          )
        );
      } catch (err) {
        setError(err.message);
      }
    }

    fetchTimeline();
  }, [investigationId]);

  async function handleTimelineSubmit(e) {
    e.preventDefault();

    setMessage("");
    setError("");

    if (!investigationId) {
      setError("Investigation is not ready yet.");
      return;
    }

    setSaving(true);

    try {
      const newEntry = await apiRequest("/investigations/timeline/", {
        method: "POST",
        body: JSON.stringify({
          investigation: investigationId,
          place,
          description,
          visited_at: visitedAt,
        }),
      });

      setTimelineEntries((previous) => [...previous, newEntry]);

      setMessage("Timeline entry added successfully!");
      setPlace("");
      setDescription("");
      setVisitedAt("");
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  async function handleAnalysis() {
    setError("");
    setAnalysis("");
    setAnalysisLoading(true);

    try {
      const data = await apiRequest("/investigations/ai-analysis/", {
        method: "POST",
        body: JSON.stringify({
          investigation: investigationId,
        }),
      });

      setAnalysis(data.analysis);
      setAnalysisSource(data.source);
    } catch (err) {
      setError(err.message);
    } finally {
      setAnalysisLoading(false);
    }
  }

  return (
    <>
      <Navbar />

      <main className="investigation-page">
        <div className="investigation-container">
          <Link to={`/report/lost/${id}/results`} className="back-link">
            ← Back to Match Results
          </Link>

          <h1>Lost Item Investigation</h1>

          <p>
            Let's investigate your missing item. Add the places you visited
            and what happened so we can help identify possible leads.
          </p>

          <section className="timeline-section">
            <h2>Your Journey Timeline</h2>

            <p>
              Remember where you went after you last saw your item.
              Add those details below.
            </p>

            {message && <p>{message}</p>}
            {error && <p className="form-error">{error}</p>}

            <TimelineForm
              place={place}
              setPlace={setPlace}
              description={description}
              setDescription={setDescription}
              visitedAt={visitedAt}
              setVisitedAt={setVisitedAt}
              handleTimelineSubmit={handleTimelineSubmit}
              saving={saving}
              investigationId={investigationId}
            />

            <TimelineList timelineEntries={timelineEntries} />
          </section>

          <AIAnalysis
            handleAnalysis={handleAnalysis}
            loading={analysisLoading}
            analysis={analysis}
            source={analysisSource}
          />
        </div>
      </main>

      <Footer />
    </>
  );
}

export default Investigation;
