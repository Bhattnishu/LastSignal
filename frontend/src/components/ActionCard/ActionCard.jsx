
import { Link, useNavigate } from "react-router-dom";
import "./ActionCard.css";

function ActionCard({ to, variant, icon, title, text, cta }) {
  const navigate = useNavigate();

  function handleClick(e) {
    const token = localStorage.getItem("access_token");

    if (!token) {
      e.preventDefault();
      navigate("/login", {
        state: { from: to },
      });
    }
  }

  return (
    <Link
      to={to}
      onClick={handleClick}
      className={`action-card ${variant}`}
    >
      <span className="card-icon">{icon}</span>
      <h2>{title}</h2>
      <p>{text}</p>
      <span className="card-link">{cta}</span>
    </Link>
  );
}

export default ActionCard;
