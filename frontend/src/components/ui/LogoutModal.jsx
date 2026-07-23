function LogoutModal({ isOpen, onCancel, onConfirm }) {
  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" role="presentation">
      <section className="logout-modal" role="dialog" aria-modal="true" aria-labelledby="logout-title">
        <div className="logout-modal-icon" aria-hidden="true">!</div>
        <h2 id="logout-title">Log out of your account?</h2>
        <p>You will need to sign in again to access your GeoAsset workspace.</p>
        <div className="logout-modal-actions">
          <button className="button-secondary" type="button" onClick={onCancel}>Cancel</button>
          <button className="button-danger" type="button" onClick={onConfirm}>Log out</button>
        </div>
      </section>
    </div>
  );
}

export default LogoutModal;
