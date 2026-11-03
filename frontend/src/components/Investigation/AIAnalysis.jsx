
import "./AIAnalysis.css";

function AIAnalysis({ handleAnalysis, loading, analysis, source }) {
  return (
    <section className="ai-analysis">
      <div className="ai-heading">
        <span className="ai-icon">✦</span>
        <div>
          <h2>Investigation Assistant</h2>
          <p>
            Explore possible locations and get helpful next steps
            based on your item's journey.
          </p>
        </div>
      </div>

      <button
        className="ai-generate-btn"
        type="button"
        onClick={handleAnalysis}
        disabled={loading}
      >
        {loading ? "Analysing your investigation..." : "✦ Generate Investigation Report"}
      </button>

      {analysis && (
        <div className="analysis-result">
          <div className="result-header">
            <div>
              <span className="result-label">YOUR REPORT</span>
              <h3>Investigation Summary</h3>
            </div>

            <span className={`source-badge ${source === "gemini" ? "gemini" : "fallback"}`}>
              {source === "gemini" ? "✦ Gemini AI" : "Smart Suggestions"}
            </span>
          </div>

          <div className="result-content">
            <p>{analysis}</p>
          </div>

          <div className="result-note">
            <span>ⓘ</span>
            Suggestions are possibilities, not confirmed locations.
          </div>
        </div>
      )}
    </section>
  );
}

export default AIAnalysis;
