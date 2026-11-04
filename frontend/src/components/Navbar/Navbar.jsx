import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiRequest } from "../../services/api";
import "./Navbar.css";

function Navbar() {
  const navigate = useNavigate();

  const [notifications, setNotifications] = useState([]);
  const [showNotifications, setShowNotifications] = useState(false);

  const isLoggedIn = Boolean(localStorage.getItem("access_token"));
  const notificationRef = useRef(null);
  const unreadCount = notifications.filter(
    (notification) => !notification.is_read
  ).length;

  async function loadNotifications() {
    if (!localStorage.getItem("access_token")) return;

    try {
      const data = await apiRequest("/items/notifications/");
      setNotifications(
        Array.isArray(data) ? data : data.results || []
      );
    } catch (error) {
      console.error("Could not load notifications:", error.message);
    }
  }

  useEffect(() => {
    if (isLoggedIn) {
      loadNotifications();
    }
  }, [isLoggedIn]);
  useEffect(() => {
    function handleNotificationsUpdated() {
      loadNotifications();
    }

    window.addEventListener(
      "notifications-updated",
      handleNotificationsUpdated
    );

    return () => {
      window.removeEventListener(
        "notifications-updated",
        handleNotificationsUpdated
      );
    };
  }, []);
  useEffect(() => {
    function handleOutsideClick(event) {
      if (
        notificationRef.current &&
        !notificationRef.current.contains(event.target)
      ) {
        setShowNotifications(false);
      }
    }

    document.addEventListener("mousedown", handleOutsideClick);

    return () => {
      document.removeEventListener("mousedown", handleOutsideClick);
    };
  }, []);

  async function handleNotificationClick(notification) {
    try {
      if (!notification.is_read) {
        await apiRequest(
          `/items/notifications/${notification.id}/read/`,
          { method: "PATCH" }
        );

        setNotifications((previous) =>
          previous.map((item) =>
            item.id === notification.id
              ? { ...item, is_read: true }
              : item
          )
        );
      }

      setShowNotifications(false);

      if (notification.title === "New Recovery Request!") {
        navigate("/my-activity");
      } else {
        navigate(`/report/lost/${notification.lost_report_id}/results`);
      }
    } catch (error) {
      console.error("Notification error:", error.message);
    }
  }

  function handleLogout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    setNotifications([]);
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

            <div className="notification-wrapper" ref={notificationRef}>
              <button
                className="notification-button"
                onClick={() => {
                  setShowNotifications(!showNotifications);
                  if (!showNotifications) loadNotifications();
                }}
                aria-label="Notifications"
              >
                🔔
                {unreadCount > 0 && (
                  <span className="notification-count">
                    {unreadCount}
                  </span>
                )}
              </button>

              {showNotifications && (
                <div className="notification-dropdown">
                  <h3>Notifications</h3>

                  {notifications.length === 0 ? (
                    <p className="no-notifications">
                      No notifications yet.
                    </p>
                  ) : (
                    notifications.map((notification) => (
                      <button
                        key={notification.id}
                        className={`notification-item ${
                          notification.is_read ? "read" : "unread"
                        }`}
                        onClick={() =>
                          handleNotificationClick(notification)
                        }
                      >
                        <strong>{notification.title}</strong>
                        <p>{notification.message}</p>
                        {!notification.is_read && (
                          <span className="unread-label">New</span>
                        )}
                      </button>
                    ))
                  )}
                </div>
              )}
            </div>

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
