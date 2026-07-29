import api from "../api/axios";

// 30-second timeout for all asset-related requests
const TIMEOUT = 30000;

/**
 * Fetch all assets from the backend with filtering, sorting, and pagination
 * @param {Object} options - Query options
 * @param {string} [options.assetType] - Filter by asset type (DRONE, VEHICLE, CAMERA, SENSOR, INFRASTRUCTURE, OTHER)
 * @param {string} [options.status] - Filter by asset status (ONLINE, OFFLINE, MAINTENANCE, RETIRED)
 * @param {string} [options.search] - Search by asset name, serial number, or description
 * @param {string} [options.sortBy] - Sort field (name, created_at, updated_at, status, asset_type)
 * @param {string} [options.order] - Sort order (asc, desc)
 * @param {number} [options.limit] - Maximum number of assets to return (default: 10, max: 100)
 * @param {number} [options.offset] - Number of assets to skip (default: 0)
 * @returns {Promise<Object>} PaginatedResponse with total, limit, offset, and items array
 * @throws {Error} Network error or timeout
 */
export const getAll = async (options = {}) => {
  const {
    assetType = null,
    status = null,
    search = null,
    sortBy = "created_at",
    order = "desc",
    limit = 10,
    offset = 0,
  } = options;

  const params = new URLSearchParams();

  if (assetType) params.append("asset_type", assetType);
  if (status) params.append("status", status);
  if (search) params.append("search", search);
  params.append("sort_by", sortBy);
  params.append("order", order);
  params.append("limit", limit);
  params.append("offset", offset);

  const response = await api.get(`/assets/?${params.toString()}`, {
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
 * @param {string} data.serial_number - Asset serial number (required, 3-20 characters, must be unique)
 * @param {string} data.asset_type - Asset type (required: DRONE, VEHICLE, CAMERA, SENSOR, INFRASTRUCTURE, OTHER)
 * @param {string} [data.status] - Asset status (optional: ONLINE, OFFLINE, MAINTENANCE, RETIRED; defaults to ONLINE)
 * @param {string} data.name - Asset name (required, 3-100 characters)
 * @param {string} [data.description] - Asset description (optional, max 1000 characters)
 * @param {number} data.latitude - Latitude (required, -90 to 90)
 * @param {number} data.longitude - Longitude (required, -180 to 180)
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
 * @param {Object} data - Updated asset data (all fields optional)
 * @param {string} [data.serial_number] - Asset serial number (3-20 characters)
 * @param {string} [data.asset_type] - Asset type (DRONE, VEHICLE, CAMERA, SENSOR, INFRASTRUCTURE, OTHER)
 * @param {string} [data.status] - Asset status (ONLINE, OFFLINE, MAINTENANCE, RETIRED)
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
 * @returns {Promise<Object>} Response object with message
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
