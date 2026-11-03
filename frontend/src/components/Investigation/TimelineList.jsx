
function TimelineList({ timelineEntries }) {
  return (
    <section className="timeline-entries">
      <h3>Your Journey</h3>

      {timelineEntries.length === 0 ? (
        <p>No timeline entries added yet.</p>
      ) : (
        timelineEntries.map((entry) => (
          <div className="timeline-entry" key={entry.id}>
            <h4>{entry.place}</h4>

            {entry.description && <p>{entry.description}</p>}

            {entry.visited_at && (
              <small>
                {new Date(entry.visited_at).toLocaleString()}
              </small>
            )}
          </div>
        ))
      )}
    </section>
  );
}

export default TimelineList;
