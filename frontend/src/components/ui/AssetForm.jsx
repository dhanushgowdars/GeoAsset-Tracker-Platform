import { useState } from "react";

// Backend enum values
const ASSET_TYPES = ["DRONE", "VEHICLE", "CAMERA", "SENSOR", "INFRASTRUCTURE", "OTHER"];
const ASSET_STATUS = ["ONLINE", "OFFLINE", "MAINTENANCE", "RETIRED"];

function AssetForm({ onSubmit, onCancel, isLoading, error, initialData, mode = "create" }) {
  // Initialize form data based on mode and initialData
  const getInitialFormData = () => {
    if (mode === "edit" && initialData) {
      return {
        serial_number: initialData.serial_number || "",
        asset_type: initialData.asset_type || "",
        status: initialData.status || "ONLINE",
        name: initialData.name || "",
        description: initialData.description || "",
        latitude: initialData.latitude !== undefined ? String(initialData.latitude) : "",
        longitude: initialData.longitude !== undefined ? String(initialData.longitude) : "",
      };
    }
    return {
      serial_number: "",
      asset_type: "",
      status: "ONLINE",
      name: "",
      description: "",
      latitude: "",
      longitude: "",
    };
  };

  const [formData, setFormData] = useState(getInitialFormData);

  const [errors, setErrors] = useState({});

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    
    // Clear error for this field when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: "" }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    // Serial Number validation (3-20 chars)
    if (!formData.serial_number.trim()) {
      newErrors.serial_number = "Serial number is required";
    } else if (formData.serial_number.trim().length < 3) {
      newErrors.serial_number = "Serial number must be at least 3 characters";
    } else if (formData.serial_number.trim().length > 20) {
      newErrors.serial_number = "Serial number must not exceed 20 characters";
    }

    // Asset Type validation
    if (!formData.asset_type) {
      newErrors.asset_type = "Asset type is required";
    } else if (!ASSET_TYPES.includes(formData.asset_type)) {
      newErrors.asset_type = "Invalid asset type";
    }

    // Status validation
    if (!formData.status) {
      newErrors.status = "Status is required";
    } else if (!ASSET_STATUS.includes(formData.status)) {
      newErrors.status = "Invalid status";
    }

    // Name validation (3-100 chars)
    if (!formData.name.trim()) {
      newErrors.name = "Asset name is required";
    } else if (formData.name.trim().length < 3) {
      newErrors.name = "Asset name must be at least 3 characters";
    } else if (formData.name.trim().length > 100) {
      newErrors.name = "Asset name must not exceed 100 characters";
    }

    // Description validation (optional, but max length if provided)
    if (formData.description.trim().length > 1000) {
      newErrors.description = "Description must not exceed 1000 characters";
    }

    // Latitude validation
    if (!formData.latitude) {
      newErrors.latitude = "Latitude is required";
    } else {
      const lat = Number(formData.latitude);
      if (Number.isNaN(lat)) {
        newErrors.latitude = "Latitude must be a valid number";
      } else if (lat < -90 || lat > 90) {
        newErrors.latitude = "Latitude must be between -90 and 90";
      }
    }

    // Longitude validation
    if (!formData.longitude) {
      newErrors.longitude = "Longitude is required";
    } else {
      const lon = Number(formData.longitude);
      if (Number.isNaN(lon)) {
        newErrors.longitude = "Longitude must be a valid number";
      } else if (lon < -180 || lon > 180) {
        newErrors.longitude = "Longitude must be between -180 and 180";
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!validateForm()) {
      return;
    }

    const submitData = {
      serial_number: formData.serial_number.trim(),
      asset_type: formData.asset_type,
      status: formData.status,
      name: formData.name.trim(),
      description: formData.description.trim() || undefined,
      latitude: Number(formData.latitude),
      longitude: Number(formData.longitude),
    };

    onSubmit(submitData);
  };

  const isEditMode = mode === "edit";

  return (
    <form className="asset-form" onSubmit={handleSubmit}>
      <h2 id="asset-modal-title">{isEditMode ? "Edit Asset" : "Create New Asset"}</h2>
      <p className="asset-form-subtitle">
        {isEditMode
          ? "Update the asset details and location coordinates."
          : "Add a new asset to your account with all required information."}
      </p>

      {error && (
        <p className="form-alert" role="alert">
          {error}
        </p>
      )}

      <div className="asset-form-field">
        <label htmlFor="asset-serial-number">
          Serial Number <span className="field-required">*</span>
        </label>
        <input
          id="asset-serial-number"
          name="serial_number"
          type="text"
          value={formData.serial_number}
          onChange={handleChange}
          disabled={isLoading || (isEditMode && initialData)}
          placeholder="e.g., SN-001"
          aria-invalid={errors.serial_number ? "true" : "false"}
          aria-describedby={errors.serial_number ? "serial_number-error" : undefined}
        />
        {errors.serial_number && (
          <p id="serial_number-error" className="field-error" role="alert">
            {errors.serial_number}
          </p>
        )}
      </div>

      <div className="asset-form-row">
        <div className="asset-form-field">
          <label htmlFor="asset-type">
            Asset Type <span className="field-required">*</span>
          </label>
          <select
            id="asset-type"
            name="asset_type"
            value={formData.asset_type}
            onChange={handleChange}
            disabled={isLoading}
            aria-invalid={errors.asset_type ? "true" : "false"}
            aria-describedby={errors.asset_type ? "asset_type-error" : undefined}
          >
            <option value="">Select an asset type</option>
            {ASSET_TYPES.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
          {errors.asset_type && (
            <p id="asset_type-error" className="field-error" role="alert">
              {errors.asset_type}
            </p>
          )}
        </div>

        <div className="asset-form-field">
          <label htmlFor="asset-status">
            Status <span className="field-required">*</span>
          </label>
          <select
            id="asset-status"
            name="status"
            value={formData.status}
            onChange={handleChange}
            disabled={isLoading}
            aria-invalid={errors.status ? "true" : "false"}
            aria-describedby={errors.status ? "status-error" : undefined}
          >
            {ASSET_STATUS.map((status) => (
              <option key={status} value={status}>
                {status}
              </option>
            ))}
          </select>
          {errors.status && (
            <p id="status-error" className="field-error" role="alert">
              {errors.status}
            </p>
          )}
        </div>
      </div>

      <div className="asset-form-field">
        <label htmlFor="asset-name">
          Asset Name <span className="field-required">*</span>
        </label>
        <input
          id="asset-name"
          name="name"
          type="text"
          value={formData.name}
          onChange={handleChange}
          disabled={isLoading}
          placeholder="e.g., Surveillance Camera 01"
          aria-invalid={errors.name ? "true" : "false"}
          aria-describedby={errors.name ? "name-error" : undefined}
        />
        {errors.name && (
          <p id="name-error" className="field-error" role="alert">
            {errors.name}
          </p>
        )}
      </div>

      <div className="asset-form-field">
        <label htmlFor="asset-description">Description</label>
        <textarea
          id="asset-description"
          name="description"
          rows="3"
          value={formData.description}
          onChange={handleChange}
          disabled={isLoading}
          placeholder="Optional description"
          aria-invalid={errors.description ? "true" : "false"}
          aria-describedby={errors.description ? "description-error" : undefined}
        />
        {errors.description && (
          <p id="description-error" className="field-error" role="alert">
            {errors.description}
          </p>
        )}
      </div>

      <div className="asset-form-row">
        <div className="asset-form-field">
          <label htmlFor="asset-latitude">
            Latitude <span className="field-required">*</span>
          </label>
          <input
            id="asset-latitude"
            name="latitude"
            type="text"
            inputMode="decimal"
            placeholder="-90 to 90"
            value={formData.latitude}
            onChange={handleChange}
            disabled={isLoading}
            aria-invalid={errors.latitude ? "true" : "false"}
            aria-describedby={errors.latitude ? "latitude-error" : undefined}
          />
          {errors.latitude && (
            <p id="latitude-error" className="field-error" role="alert">
              {errors.latitude}
            </p>
          )}
        </div>

        <div className="asset-form-field">
          <label htmlFor="asset-longitude">
            Longitude <span className="field-required">*</span>
          </label>
          <input
            id="asset-longitude"
            name="longitude"
            type="text"
            inputMode="decimal"
            placeholder="-180 to 180"
            value={formData.longitude}
            onChange={handleChange}
            disabled={isLoading}
            aria-invalid={errors.longitude ? "true" : "false"}
            aria-describedby={errors.longitude ? "longitude-error" : undefined}
          />
          {errors.longitude && (
            <p id="longitude-error" className="field-error" role="alert">
              {errors.longitude}
            </p>
          )}
        </div>
      </div>

      <div className="asset-form-actions">
        <button
          className="button-secondary"
          type="button"
          onClick={onCancel}
          disabled={isLoading}
        >
          Cancel
        </button>
        <button className="button-primary" type="submit" disabled={isLoading}>
          {isLoading ? (
            <>
              <span className="button-spinner" aria-hidden="true" />
              {isEditMode ? "Updating..." : "Creating..."}
            </>
          ) : (
            isEditMode ? "Update Asset" : "Create Asset"
          )}
        </button>
      </div>
    </form>
  );
}

export default AssetForm;
