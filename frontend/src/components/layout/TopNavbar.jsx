import { useState } from "react";

const getInitials = (username) => username?.slice(0, 1).toUpperCase() || "U";

function TopNavbar({ pageTitle, user, onMenuToggle, onLogout }) {
  const [isProfileOpen, setIsProfileOpen] = useState(false);

  return (
    <header className="top-navbar">
      <button className="menu-toggle" type="button" onClick={onMenuToggle} aria-label="Open navigation">
        <span />
        <span />
        <span />
      </button>
      <div>
        <p className="top-navbar-project">GeoAsset Tracker Platform</p>
        <h1>{pageTitle}</h1>
      </div>
      <div className="profile-menu">
        <button
          className="profile-button"
          type="button"
          onClick={() => setIsProfileOpen((isOpen) => !isOpen)}
          aria-expanded={isProfileOpen}
          aria-haspopup="menu"
        >
          <span className="profile-avatar" aria-hidden="true">{getInitials(user?.username)}</span>
          <span className="profile-label">{user?.username || "Profile"}</span>
          <span className="profile-chevron" aria-hidden="true">⌄</span>
        </button>
        {isProfileOpen && (
          <div className="profile-dropdown" role="menu">
            <div className="profile-dropdown-details">
              <strong>{user?.username || "Profile"}</strong>
              <span>{user?.email || "Loading profile..."}</span>
            </div>
            <button type="button" role="menuitem" onClick={() => { setIsProfileOpen(false); onLogout(); }}>
              Log out
            </button>
          </div>
        )}
      </div>
    </header>
  );
}

export default TopNavbar;
