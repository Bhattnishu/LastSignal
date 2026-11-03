
function TimelineForm({
  place,
  setPlace,
  description,
  setDescription,
  visitedAt,
  setVisitedAt,
  handleTimelineSubmit,
  saving,
  investigationId,
}) {
  return (
    <form onSubmit={handleTimelineSubmit} className="timeline-form">
      <input
        type="text"
        placeholder="Place visited"
        value={place}
        onChange={(e) => setPlace(e.target.value)}
        required
      />

      <textarea
        placeholder="What happened there? (Optional)"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />

      <input
        type="datetime-local"
        value={visitedAt}
        onChange={(e) => setVisitedAt(e.target.value)}
      />

      <button type="submit" disabled={saving || !investigationId}>
        {saving ? "Saving..." : "Add Timeline Entry"}
      </button>
    </form>
  );
}

export default TimelineForm;
