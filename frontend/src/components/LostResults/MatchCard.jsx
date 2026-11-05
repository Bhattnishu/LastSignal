function MatchCard({ match, requestStatus, getRequestLabel, onContact }) {
  const report = match.report;

  return (
    <div className="match-card" key={report.id}>
      <div className="match-card-header">
        <div>
          <h2>{report.item_name}</h2>
          <p>{report.location}, {report.city}</p>
        </div>

        <span className="match-score">
          {match.match_score}% Match
        </span>
      </div>

      {report.image && (
        <img
          src={report.image}
          alt={report.item_name}
          className="matched-item-image"
        />
      )}

      <details className="match-details">
        <summary>View item details and match reasons</summary>

        <p>Category: {report.category}</p>
        <p>Brand: {report.brand || "Not specified"}</p>
        <p>Color: {report.color || "Not specified"}</p>

        <p>Why it may match:</p>
        <ul>
          {match.match_reasons.map((reason, index) => (
            <li key={index}>{reason}</li>
          ))}
        </ul>
      </details>

      {requestStatus ? (
        <p className="recovery-success">
          {getRequestLabel(requestStatus)}
        </p>
      ) : (
        <button
          className="recovery-request-btn"
          onClick={() => onContact(match)}
        >
          Contact Finder
        </button>
      )}
    </div>
  );
}

export default MatchCard;