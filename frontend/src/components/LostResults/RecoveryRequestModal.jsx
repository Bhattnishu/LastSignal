function RecoveryRequestModal({
  selectedMatch,
  message,
  setMessage,
  contactMethod,
  setContactMethod,
  contactValue,
  setContactValue,
  sending,
  error,
  onClose,
  onSubmit,
}) {
  if (!selectedMatch) return null;

  return (
    <div className="recovery-modal-overlay">
      <div className="recovery-modal">
        <h2>Contact Finder</h2>

        <p>
          Explain why you believe this{" "}
          {selectedMatch.report.item_name} belongs to you and
          share your contact details.
        </p>

        <form onSubmit={onSubmit}>
          <textarea
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Explain why this item belongs to you..."
            rows={4}
            required
          />

          <select
            value={contactMethod}
            onChange={(e) => setContactMethod(e.target.value)}
          >
            <option value="PHONE">Phone Number</option>
            <option value="EMAIL">Email Address</option>
          </select>

          <input
            type={contactMethod === "EMAIL" ? "email" : "tel"}
            value={contactValue}
            onChange={(e) => setContactValue(e.target.value)}
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
              onClick={onClose}
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
  );
}

export default RecoveryRequestModal;