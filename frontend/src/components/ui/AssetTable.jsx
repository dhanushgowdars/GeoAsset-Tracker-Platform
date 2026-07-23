const formatCoordinates = (value) => (Number.isFinite(Number(value)) ? Number(value).toFixed(5) : "—");

const formatDate = (value) => {
  if (!value) return "—";

  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? "—"
    : new Intl.DateTimeFormat(undefined, { dateStyle: "medium", timeStyle: "short" }).format(date);
};

const getOwner = (asset) => asset.owner?.username || asset.owner_name || asset.owner_id || "—";

function AssetTable({ assets, isLoading, error, onRetry, searchTerm }) {
  if (isLoading) {
    return (
      <div className="asset-table-wrap" aria-label="Loading assets" aria-busy="true">
        <table className="asset-table asset-table-skeleton">
          <thead><tr><th>Name</th><th>Description</th><th>Latitude</th><th>Longitude</th><th>Owner</th><th>Created at</th></tr></thead>
          <tbody>
            {[0, 1, 2, 3, 4].map((row) => (
              <tr key={row}><td><span /></td><td><span /></td><td><span /></td><td><span /></td><td><span /></td><td><span /></td></tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  if (error) {
    return (
      <div className="asset-state asset-error" role="alert">
        <strong>Unable to load assets</strong>
        <p>{error}</p>
        <button type="button" onClick={onRetry}>Try again</button>
      </div>
    );
  }

  if (!assets.length) {
    return (
      <div className="asset-state">
        <strong>{searchTerm ? "No matching assets" : "No assets yet"}</strong>
        <p>{searchTerm ? "Try a different search term." : "Assets created for your account will appear here."}</p>
      </div>
    );
  }

  return (
    <div className="asset-table-wrap">
      <table className="asset-table">
        <thead>
          <tr><th>Name</th><th>Description</th><th>Latitude</th><th>Longitude</th><th>Owner</th><th>Created at</th></tr>
        </thead>
        <tbody>
          {assets.map((asset) => (
            <tr key={asset.id}>
              <td data-label="Name"><strong>{asset.name}</strong></td>
              <td data-label="Description">{asset.description || "—"}</td>
              <td data-label="Latitude">{formatCoordinates(asset.latitude)}</td>
              <td data-label="Longitude">{formatCoordinates(asset.longitude)}</td>
              <td data-label="Owner">{getOwner(asset)}</td>
              <td data-label="Created at">{formatDate(asset.created_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AssetTable;
