
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Navbar from "../components/Navbar/Navbar";
import Footer from "../components/Footer/Footer";
import { apiRequest } from "../services/api";
import "./ReportLost.css";

function ReportLost() {
  const navigate = useNavigate();

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    const formElement = e.currentTarget;

    if (!localStorage.getItem("access_token")) {
      navigate("/login", {
        state: { from: "/report/lost" },
      });
      return;
    }

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const formData = new FormData(e.currentTarget);

      formData.append("report_type", "LOST");

      const data = await apiRequest("/items/reports/", {
        method: "POST",
        body: formData,
      });

      navigate(`/report/lost/${data.id}/results`);

      setSuccess("Your lost item report was submitted successfully!");
      formElement.reset();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Navbar />

      <div className="report-lost-page">
        <div className="report-lost-container">
          <Link to="/" className="back-link">
            ← Back to Home
          </Link>

          <h1>Report a Lost Item</h1>

          <p>
            Tell us about the item you lost.
            We'll help you find possible matches.
          </p>

          <form className="report-form" onSubmit={handleSubmit}>
            <label>Item Name</label>
            <input
              type="text"
              name="item_name"
              placeholder="e.g. Black Samsung phone"
              required
            />

            <label>Category</label>
            <select name="category" required defaultValue="">
              <option value="">Select category</option>
              <option value="ELECTRONICS">Electronics</option>
              <option value="BAGS">Bags</option>
              <option value="DOCUMENTS">Documents</option>
              <option value="CLOTHING">Clothing</option>
              <option value="ACCESSORIES">Accessories</option>
              <option value="JEWELLERY">Jewellery</option>
              <option value="OTHER">Other</option>
            </select>

            <label>Description</label>
            <textarea
              name="description"
              placeholder="Describe your lost item..."
              rows="4"
              required
            />

            <label>Brand</label>
            <input
              type="text"
              name="brand"
              placeholder="e.g. Samsung"
            />

            <label>Color</label>
            <input
              type="text"
              name="color"
              placeholder="e.g. Black"
            />

            <label>Item Image (optional)</label>
            <input type="file" name="image" accept="image/*" />

            <label>Lost Location</label>
            <input
              type="text"
              name="location"
              placeholder="Where did you lose it?"
              required
            />

            <label>City</label>
            <input
              type="text"
              name="city"
              placeholder="Enter city"
              required
            />

            <label>Date and Time Lost</label>
            <input
              type="datetime-local"
              name="occurred_at"
              required
            />

            {error && <p className="form-error">{error}</p>}
            {success && <p className="form-success">{success}</p>}

            <button type="submit" disabled={loading}>
              {loading ? "Submitting..." : "Find My Item"}
            </button>
          </form>
        </div>
      </div>

      <div className="report-lost-footer-container">
        <Footer />
      </div>
    </>
  );
}

export default ReportLost;
