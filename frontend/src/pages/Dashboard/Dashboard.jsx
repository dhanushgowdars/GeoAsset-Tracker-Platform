import { useNavigate } from "react-router-dom";

import { removeToken } from "../../utils/storage";
import "./Dashboard.css";

function Dashboard() {
  const navigate = useNavigate();

  const handleLogout = () => {
    removeToken();
    navigate("/", { replace: true });
  };

  return (
    <main className="dashboard-page">
      <header className="dashboard-header">
        <div className="dashboard-brand">
          <span className="dashboard-mark" aria-hidden="true">GA</span>
          <span>GeoAsset Tracker</span>
        </div>
        <button className="logout-button" type="button" onClick={handleLogout}>
          Log out
        </button>
      </header>

      <section className="dashboard-content" aria-labelledby="dashboard-title">
        <p className="dashboard-eyebrow">Dashboard</p>
        <h1 id="dashboard-title">Welcome to your GeoAsset workspace.</h1>
        <p>
          Your account is signed in and ready to help you monitor, organize, and explore your
          assets.
        </p>
      </section>
    </main>
  );
}

export default Dashboard;
