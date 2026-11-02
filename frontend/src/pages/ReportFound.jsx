
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import Navbar from "../components/Navbar/Navbar";
import Footer from "../components/Footer/Footer";
import { apiRequest } from "../services/api";
import "./ReportLost.css";

function ReportFound() {
  const navigate = useNavigate();

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();

    if (!localStorage.getItem("access_token")) {
      navigate("/login", {
        state: { from: "/report/found" },
      });
      return;
    }

    setError("");
    setLoading(true);

    try {
      const formData = new FormData(e.currentTarget);
      formData.append("report_type", "FOUND");

      await apiRequest("/items/reports/", {
        method: "POST",
        body: formData,
      });

      navigate("/");
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

          <h1>Report a Found Item</h1>

          <p>
            Found something that someone might have lost?
            Share its details to help reunite it with its owner.
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
              placeholder="Describe the item you found..."
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
            <input
              type="file"
              name="image"
              accept="image/*"
            />

            <label>Found Location</label>
            <input
              type="text"
              name="location"
              placeholder="Where did you find it?"
              required
            />

            <label>City</label>
            <input
              type="text"
              name="city"
              placeholder="Enter city"
              required
            />

            <label>Date and Time Found</label>
            <input
              type="datetime-local"
              name="occurred_at"
              required
            />

            {error && <p className="form-error">{error}</p>}

            <button type="submit" disabled={loading}>
              {loading ? "Submitting..." : "Submit Found Item"}
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

export default ReportFound;
