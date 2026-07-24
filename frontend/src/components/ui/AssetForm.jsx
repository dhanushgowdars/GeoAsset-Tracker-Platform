import { useState } from "react";

function AssetForm({ onSubmit, onCancel, isLoading, error, initialData, mode = "create" }) {
  // Initialize form data based on mode and initialData
  const getInitialFormData = () => {
    if (mode === "edit" && initialData) {
      return {
        name: initialData.name || "",
        description: initialData.description || "",
        latitude: initialData.latitude !== undefined ? String(initialData.latitude) : "",
        longitude: initialData.longitude !== undefined ? String(initialData.longitude) : "",
      };
    }
    return {
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

    // Name validation
    if (!formData.name.trim()) {
      newErrors.name = "Asset name is required";
    } else if (formData.name.trim().length < 3) {
      newErrors.name = "Asset name must be at least 3 characters";
    } else if (formData.name.trim().length > 100) {
      newErrors.name = "Asset name must not exceed 100 characters";
    }

    // Description validation
    if (formData.description.length > 1000) {
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
          : "Add a new asset to your account with location coordinates."}
      </p>

      {error && (
        <p className="form-alert" role="alert">
          {error}
        </p>
      )}

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
