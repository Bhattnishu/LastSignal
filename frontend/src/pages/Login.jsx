import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiRequest } from "../services/api";
import "./Auth.css";
import Navbar from "../components/Navbar/Navbar";

function Login() {
  const navigate = useNavigate();

const [form, setForm] = useState({
  email: "",
  password: "",
});

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const data = await apiRequest("/auth/login/", {
        method: "POST",
        body: JSON.stringify(form),
      });

      localStorage.setItem("access_token", data.access);
      localStorage.setItem("refresh_token", data.refresh);

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
    <div className="auth-page">
      <div className="auth-container">
        <h1>Welcome Back</h1>
        <p>Sign in to continue your LastSignal journey.</p>

        <form onSubmit={handleSubmit}>
          <input
            name="email"
            type="email"
            placeholder="Email address"
            value={form.email}
            onChange={handleChange}
            required
          />

          <input
            name="password"
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={handleChange}
            required
          />

          {error && <p className="auth-error">{error}</p>}

          <button type="submit" disabled={loading}>
            {loading ? "Signing in..." : "Login"}
          </button>
        </form>

        <p>
          Don't have an account? <Link to="/register">Register</Link>
        </p>
      </div>
    </div>
    </>
  );
}

export default Login;