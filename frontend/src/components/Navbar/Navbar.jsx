
import { Link, useNavigate } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  const navigate = useNavigate();
  const isLoggedIn = Boolean(localStorage.getItem("access_token"));

  function handleLogout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    navigate("/");
  }

  return (
    <nav className="navbar">
      <Link to="/" className="logo">
        🎃 LastSignal
      </Link>

      <div className="nav-auth">
        {isLoggedIn ? (
          <>
            <Link to="/my-activity" className="nav-button login-btn">
              My Activity
            </Link>

            <Link to="/profile" className="nav-button login-btn">
              My Profile
            </Link>

            <button onClick={handleLogout} className="nav-button logout-btn">
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="nav-button login-btn">
              Login
            </Link>

            <Link to="/register" className="nav-button signup-btn">
              Sign Up
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
