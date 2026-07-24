function AssetModal({ isOpen, onClose, children }) {
  if (!isOpen) return null;

  const handleBackdropClick = (event) => {
    if (event.target === event.currentTarget) {
      onClose();
    }
  };

  return (
    <div className="modal-backdrop" role="presentation" onClick={handleBackdropClick}>
      <section className="asset-modal" role="dialog" aria-modal="true" aria-labelledby="asset-modal-title">
        {children}
      </section>
    </div>
  );
}

export default AssetModal;
