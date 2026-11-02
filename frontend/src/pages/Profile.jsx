
import { useEffect, useState } from "react";
import Navbar from "../components/Navbar/Navbar";
import Footer from "../components/Footer/Footer";
import { apiRequest } from "../services/api";
import "./Profile.css";

function Profile() {
  const [profile, setProfile] = useState(null);
  const [form, setForm] = useState({ name: "", phone: "" });
  const [editing, setEditing] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchProfile() {
      try {
        const data = await apiRequest("/auth/me/");
        setProfile(data);
        setForm({ name: data.name, phone: data.phone });
      } catch (err) {
        setError(err.message);
      }
    }

    fetchProfile();
  }, []);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }
  
  async function handleSave() {
    setError("");

    try {
        const data = await apiRequest("/auth/me/", {
        method: "PATCH",
        body: JSON.stringify(form),
        });

        setProfile(data);
        setForm({
        name: data.name,
        phone: data.phone,
        });

        setEditing(false);
    } catch (err) {
        setError(err.message);
    }
    }

  function handleCancel() {
    setForm({ name: profile.name, phone: profile.phone });
    setEditing(false);
    setError("");
  }
  async function handleDeleteAccount() {
    const confirmed = window.confirm(
        "Are you sure you want to permanently delete your account? This action cannot be undone."
    );

    if (!confirmed) {
        return;
    }

    try {
        await apiRequest("/auth/delete/", {
        method: "DELETE",
        });

        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");

        window.location.href = "/";
    } catch (err) {
        setError(err.message);
    }
    }

  return (
    <>
      <Navbar />

      <div className="profile-page">
        <div className="profile-container">
          <h1>My Profile</h1>

          {error && <p className="form-error">{error}</p>}

          {!profile && !error && <p>Loading profile...</p>}

          {profile && (
            <>
              <div className="profile-field">
                <label>Name</label>
                {editing ? (
                  <input
                    name="name"
                    value={form.name}
                    onChange={handleChange}
                  />
                ) : (
                  <p>{profile.name}</p>
                )}
              </div>

              <div className="profile-field">
                <label>Email</label>
                <p>{profile.email}</p>
              </div>

              <div className="profile-field">
                <label>Phone</label>
                {editing ? (
                  <input
                    name="phone"
                    value={form.phone}
                    onChange={handleChange}
                  />
                ) : (
                  <p>{profile.phone}</p>
                )}
              </div>

              {editing ? (
                <div className="profile-actions">
                  <button type="button" onClick={handleSave}>
                    Save Changes
                  </button>
                  <button type="button" onClick={handleCancel}>
                    Cancel
                  </button>
                </div>
              ) : (
                <button
                  type="button"
                  onClick={() => setEditing(true)}
                >
                  Edit Profile
                </button>
              )}
              <div className="delete-account-section">
                <button
                    type="button"
                    className="delete-account-btn"
                    onClick={handleDeleteAccount}
                >
                    Delete Account
                </button>
                </div>
            </>
          )}
        </div>
      </div>

      <Footer />
    </>
  );
}

export default Profile;
