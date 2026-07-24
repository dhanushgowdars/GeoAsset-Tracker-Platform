function DeleteConfirmModal({ isOpen, onCancel, onConfirm, assetName, isDeleting }) {
  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" role="presentation">
      <section className="delete-confirm-modal" role="dialog" aria-modal="true" aria-labelledby="delete-confirm-title">
        <div className="delete-confirm-icon" aria-hidden="true">!</div>
        <h2 id="delete-confirm-title">Delete Asset</h2>
        <p>
          Are you sure you want to delete{" "}
          <strong>{assetName}</strong>?
        </p>
        <p className="delete-warning">This action cannot be undone.</p>
        <div className="delete-confirm-actions">
          <button
            className="button-secondary"
            type="button"
            onClick={onCancel}
            disabled={isDeleting}
          >
            Cancel
          </button>
          <button
            className="button-danger"
            type="button"
            onClick={onConfirm}
            disabled={isDeleting}
          >
            {isDeleting ? (
              <>
                <span className="button-spinner" aria-hidden="true" />
                Deleting...
              </>
            ) : (
              "Delete"
            )}
          </button>
        </div>
      </section>
    </div>
  );
}

export default DeleteConfirmModal;
