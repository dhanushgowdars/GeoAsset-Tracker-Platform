import api from "../api/axios";

export const getAssets = async () => {
  const response = await api.get("/assets/");
  return response.data;
};
