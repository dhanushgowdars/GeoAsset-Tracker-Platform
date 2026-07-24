import api from "../api/axios";

// 30-second timeout for all asset-related requests
const TIMEOUT = 30000;

/**
 * Fetch all assets from the backend
 * @returns {Promise<Array>} Array of asset objects
 * @throws {Error} Network error or timeout
 */
export const getAll = async () => {
  const response = await api.get("/assets/", {
    timeout: TIMEOUT,
  });
  return response.data;
};

/**
 * Fetch a single asset by ID
 * @param {number|string} id - Asset ID
 * @returns {Promise<Object>} Asset object
 * @throws {Error} Network error, timeout, or 404 if asset not found
 */
export const getById = async (id) => {
  const response = await api.get(`/assets/${id}`, {
    timeout: TIMEOUT,
  });
  return response.data;
};

/**
 * Create a new asset
 * @param {Object} data - Asset data
 * @param {string} data.name - Asset name (required, 3-100 characters)
 * @param {string} [data.description] - Asset description (optional, max 1000 characters)
 * @param {number} data.latitude - Latitude (-90 to 90)
 * @param {number} data.longitude - Longitude (-180 to 180)
 * @returns {Promise<Object>} Created asset object
 * @throws {Error} Network error, timeout, or validation error
 */
export const create = async (data) => {
  const response = await api.post("/assets/", data, {
    timeout: TIMEOUT,
  });
  return response.data;
};

/**
 * Update an existing asset
 * @param {number|string} id - Asset ID
 * @param {Object} data - Updated asset data
 * @param {string} [data.name] - Asset name (3-100 characters)
 * @param {string} [data.description] - Asset description (max 1000 characters)
 * @param {number} [data.latitude] - Latitude (-90 to 90)
 * @param {number} [data.longitude] - Longitude (-180 to 180)
 * @returns {Promise<Object>} Updated asset object
 * @throws {Error} Network error, timeout, validation error, or 404 if asset not found
 */
export const update = async (id, data) => {
  const response = await api.put(`/assets/${id}`, data, {
    timeout: TIMEOUT,
  });
  return response.data;
};

/**
 * Delete an asset
 * @param {number|string} id - Asset ID
 * @returns {Promise<void>}
 * @throws {Error} Network error, timeout, 404 if asset not found, or 403 if not authorized
 */
export const deleteAsset = async (id) => {
  const response = await api.delete(`/assets/${id}`, {
    timeout: TIMEOUT,
  });
  return response.data;
};

// Legacy export for backward compatibility
export const getAssets = getAll;
