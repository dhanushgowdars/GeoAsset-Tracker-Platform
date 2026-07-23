import { useOutletContext } from "react-router-dom";

import StatCard from "../../components/ui/StatCard";

const formatLastUpdated = (assets) => {
  const dates = assets
    .map((asset) => new Date(asset.created_at))
    .filter((date) => !Number.isNaN(date.getTime()));

  if (!dates.length) return "—";

  return new Intl.DateTimeFormat(undefined, { dateStyle: "medium" }).format(
    new Date(Math.max(...dates.map((date) => date.getTime()))),
  );
};

function Dashboard() {
  const { assets, isLoadingAssets, assetsError } = useOutletContext();

  return (
    <main className="dashboard-content">
      <section className="dashboard-intro" aria-labelledby="overview-title">
        <div>
          <p className="dashboard-eyebrow">Overview</p>
          <h2 id="overview-title">Asset operations at a glance</h2>
          <p>Monitor the assets available to your account from one central workspace.</p>
        </div>
      </section>

      <section className="stats-grid" aria-label="Asset statistics">
        <StatCard label="Total Assets" value={isLoadingAssets ? "—" : assets.length} detail="Assets in your account" tone="teal" />
        <StatCard label="Online Assets" value="—" detail="Status data is not available" />
        <StatCard label="Nearby Assets" value="—" detail="Location search is coming soon" />
        <StatCard label="Last Updated" value={isLoadingAssets ? "—" : formatLastUpdated(assets)} detail="Most recently created asset" />
      </section>

      <section className="dashboard-status-card" aria-label="Workspace status">
        <div className="status-card-icon" aria-hidden="true">↗</div>
        <div>
          <h2>{assetsError ? "Asset data needs attention" : "Your workspace is ready"}</h2>
          <p>{assetsError ? "Open Assets to retry loading your latest data." : "Use the Assets page to search and review every tracked location."}</p>
        </div>
      </section>
    </main>
  );
}

export default Dashboard;
