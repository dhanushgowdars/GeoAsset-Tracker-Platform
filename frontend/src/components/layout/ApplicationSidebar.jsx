import { NavLink } from "react-router-dom";

function NavIcon({ name }) {
  const icons = {
    dashboard: <path d="M4 4h6v6H4V4Zm10 0h6v6h-6V4ZM4 14h6v6H4v-6Zm10 0h6v6h-6v-6Z" />,
    assets: <path d="M4 6.5 12 3l8 3.5v11L12 21l-8-3.5v-11ZM4 6.5 12 10l8-3.5M12 10v11" />,
    map: <path d="m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3V6Zm6-3v15m6-12v15" />,
    settings: <path d="M12 15.2a3.2 3.2 0 1 0 0-6.4 3.2 3.2 0 0 0 0 6.4Zm0-12.2v2m0 14v2m9-9h-2M5 12H3m15.4-6.4-1.4 1.4M7 17l-1.4 1.4m12.8 0L17 17M7 7 5.6 5.6" />,
    logout: <path d="M10 5H5v14h5m4-10 3 3-3 3m-7-3h10" />,
  };

  return <svg aria-hidden="true" viewBox="0 0 24 24">{icons[name]}</svg>;
}

const navigationItems = [
  { label: "Dashboard", path: "/dashboard", icon: "dashboard" },
  { label: "Assets", path: "/assets", icon: "assets" },
  { label: "Map", path: "/map", icon: "map" },
  { label: "Settings", path: "/settings", icon: "settings" },
];

function ApplicationSidebar({ isOpen, onClose, onLogout }) {
  return (
    <aside className={`app-sidebar ${isOpen ? "is-open" : ""}`} aria-label="Primary navigation">
      <div className="sidebar-brand">
        <span className="sidebar-mark" aria-hidden="true">GA</span>
        <span>GeoAsset Tracker</span>
        <button className="sidebar-close" type="button" onClick={onClose} aria-label="Close navigation">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>

      <nav className="sidebar-nav">
        {navigationItems.map((item) => (
          <NavLink
            key={item.path}
            className={({ isActive }) => `sidebar-link${isActive ? " is-active" : ""}`}
            to={item.path}
            onClick={onClose}
          >
            <NavIcon name={item.icon} />
            {item.label}
          </NavLink>
        ))}
      </nav>

      <button className="sidebar-logout" type="button" onClick={onLogout}>
        <NavIcon name="logout" />
        Log out
      </button>
    </aside>
  );
}

export default ApplicationSidebar;
