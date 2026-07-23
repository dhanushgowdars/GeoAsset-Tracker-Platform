import { useMemo, useState } from "react";
import { useOutletContext } from "react-router-dom";

import AssetTable from "../../components/ui/AssetTable";

function Assets() {
  const { assets, isLoadingAssets, assetsError, reloadAssets } = useOutletContext();
  const [searchTerm, setSearchTerm] = useState("");

  const filteredAssets = useMemo(() => {
    const normalizedTerm = searchTerm.trim().toLowerCase();
    if (!normalizedTerm) return assets;

    return assets.filter((asset) => (
      asset.name?.toLowerCase().includes(normalizedTerm)
      || asset.description?.toLowerCase().includes(normalizedTerm)
    ));
  }, [assets, searchTerm]);

  return (
    <main className="dashboard-content">
      <section className="assets-panel" aria-labelledby="assets-title">
        <div className="assets-panel-header">
          <div>
            <p className="dashboard-eyebrow">Asset Directory</p>
            <h2 id="assets-title">Your assets</h2>
            <p className="assets-panel-copy">Search and review the assets associated with your account.</p>
          </div>
          <label className="asset-search">
            <span className="sr-only">Search assets</span>
            <svg aria-hidden="true" viewBox="0 0 24 24"><circle cx="11" cy="11" r="6" /><path d="m16 16 4 4" /></svg>
            <input
              type="search"
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
              placeholder="Search name or description"
            />
          </label>
        </div>
        <AssetTable
          assets={filteredAssets}
          isLoading={isLoadingAssets}
          error={assetsError}
          onRetry={reloadAssets}
          searchTerm={searchTerm}
        />
      </section>
    </main>
  );
}

export default Assets;
