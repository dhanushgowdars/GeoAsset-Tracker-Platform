import api from "../api/axios";

export const loginUser = async (credentials) => {
  const response = await api.post("/users/login", credentials);
  return response.data;
};

export const registerUser = async (userDetails) => {
  const response = await api.post("/users/register", userDetails);
  return response.data;
};
