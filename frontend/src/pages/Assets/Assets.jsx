import { useMemo, useState } from "react";
import { useOutletContext } from "react-router-dom";

import AssetTable from "../../components/ui/AssetTable";
import AssetModal from "../../components/ui/AssetModal";
import AssetForm from "../../components/ui/AssetForm";
import DeleteConfirmModal from "../../components/ui/DeleteConfirmModal";
import { create as createAsset, update as updateAsset, deleteAsset } from "../../services/assetService";

function Assets() {
  const { assets, isLoadingAssets, assetsError, reloadAssets } = useOutletContext();
  const [searchTerm, setSearchTerm] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");
  const [showSuccess, setShowSuccess] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [modalMode, setModalMode] = useState("create");
  const [selectedAsset, setSelectedAsset] = useState(null);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [assetToDelete, setAssetToDelete] = useState(null);
  const [isDeleting, setIsDeleting] = useState(false);

  const filteredAssets = useMemo(() => {
    const normalizedTerm = searchTerm.trim().toLowerCase();
    if (!normalizedTerm) return assets;

    return assets.filter((asset) => (
      asset.name?.toLowerCase().includes(normalizedTerm)
      || asset.description?.toLowerCase().includes(normalizedTerm)
    ));
  }, [assets, searchTerm]);

  const handleOpenModal = () => {
    setModalMode("create");
    setSelectedAsset(null);
    setIsModalOpen(true);
    setSubmitError("");
  };

  const handleEditAsset = (asset) => {
    setModalMode("edit");
    setSelectedAsset(asset);
    setIsModalOpen(true);
    setSubmitError("");
  };

  const handleDeleteAsset = (asset) => {
    setAssetToDelete(asset);
    setIsDeleteModalOpen(true);
  };

  const handleCancelDelete = () => {
    if (!isDeleting) {
      setIsDeleteModalOpen(false);
      setAssetToDelete(null);
    }
  };

  const handleConfirmDelete = async () => {
    if (!assetToDelete) return;

    setIsDeleting(true);

    try {
      await deleteAsset(assetToDelete.id);
      setIsDeleteModalOpen(false);
      setSuccessMessage("Asset deleted successfully!");
      setShowSuccess(true);

      // Refresh asset list
      await reloadAssets();

      // Hide success notification after 3 seconds
      setTimeout(() => {
        setShowSuccess(false);
      }, 3000);
    } catch (err) {
      // Extract error message from backend response
      let errorMessage = "Failed to delete asset. Please try again.";

      if (err.response?.data?.detail) {
        if (typeof err.response.data.detail === "string") {
          errorMessage = err.response.data.detail;
        }
      } else if (err.message) {
        errorMessage = err.message;
      }

      // Show error in notification
      setSuccessMessage(errorMessage);
      setShowSuccess(true);
      setIsDeleteModalOpen(false);

      // Hide error notification after 5 seconds
      setTimeout(() => {
        setShowSuccess(false);
      }, 5000);
    } finally {
      setIsDeleting(false);
      setAssetToDelete(null);
    }
  };

  const handleCloseModal = () => {
    if (!isSubmitting) {
      setIsModalOpen(false);
      setSubmitError("");
      setSelectedAsset(null);
      setModalMode("create");
    }
  };

  const handleSubmit = async (data) => {
    setIsSubmitting(true);
    setSubmitError("");

    try {
      if (modalMode === "edit" && selectedAsset) {
        // Update existing asset
        await updateAsset(selectedAsset.id, data);
        setIsModalOpen(false);
        setSuccessMessage("Asset updated successfully!");
        setShowSuccess(true);
      } else {
        // Create new asset
        await createAsset(data);
        setIsModalOpen(false);
        setSuccessMessage("Asset created successfully!");
        setShowSuccess(true);
      }
      
      // Refresh asset list
      await reloadAssets();

      // Hide success notification after 3 seconds
      setTimeout(() => {
        setShowSuccess(false);
      }, 3000);
    } catch (err) {
      // Extract error message from backend response
      const action = modalMode === "edit" ? "update" : "create";
      let errorMessage = `Failed to ${action} asset. Please try again.`;
      
      if (err.response?.data?.detail) {
        if (Array.isArray(err.response.data.detail)) {
          // Validation errors from FastAPI
          errorMessage = err.response.data.detail
            .map((error) => error.msg || error.message)
            .join(". ");
        } else if (typeof err.response.data.detail === "string") {
          errorMessage = err.response.data.detail;
        }
      } else if (err.message) {
        errorMessage = err.message;
      }

      setSubmitError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="dashboard-content">
      {showSuccess && (
        <div className="success-notification" role="alert">
          <svg aria-hidden="true" viewBox="0 0 24 24">
            <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {successMessage}
        </div>
      )}

      <section className="assets-panel" aria-labelledby="assets-title">
        <div className="assets-panel-header">
          <div>
            <p className="dashboard-eyebrow">Asset Directory</p>
            <h2 id="assets-title">Your assets</h2>
            <p className="assets-panel-copy">Search and review the assets associated with your account.</p>
          </div>
          <div className="assets-panel-actions">
            <button className="button-create" type="button" onClick={handleOpenModal}>
              <svg aria-hidden="true" viewBox="0 0 24 24">
                <path d="M12 5v14m-7-7h14" />
              </svg>
              Create Asset
            </button>
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
        </div>
        <AssetTable
          assets={filteredAssets}
          isLoading={isLoadingAssets}
          error={assetsError}
          onRetry={reloadAssets}
          searchTerm={searchTerm}
          onEdit={handleEditAsset}
          onDelete={handleDeleteAsset}
        />
      </section>

      <AssetModal isOpen={isModalOpen} onClose={handleCloseModal}>
        <AssetForm
          key={modalMode === "edit" ? selectedAsset?.id : "create"}
          onSubmit={handleSubmit}
          onCancel={handleCloseModal}
          isLoading={isSubmitting}
          error={submitError}
          mode={modalMode}
          initialData={selectedAsset}
        />
      </AssetModal>

      <DeleteConfirmModal
        isOpen={isDeleteModalOpen}
        onCancel={handleCancelDelete}
        onConfirm={handleConfirmDelete}
        assetName={assetToDelete?.name || "this asset"}
        isDeleting={isDeleting}
      />
    </main>
  );
}

export default Assets;
