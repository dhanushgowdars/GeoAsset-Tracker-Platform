const emailPattern = /^\S+@\S+\.\S+$/;

export const validateLoginForm = ({ email, password }) => {
  const errors = {};

  if (!email.trim()) errors.email = "Email is required.";
  else if (!emailPattern.test(email)) errors.email = "Enter a valid email address.";

  if (!password) errors.password = "Password is required.";
  else if (password.length < 8) errors.password = "Password must be at least 8 characters.";

  return errors;
};

export const validateRegistrationForm = ({ username, email, password, confirmPassword }) => {
  const errors = validateLoginForm({ email, password });

  if (!username.trim()) errors.username = "Username is required.";

  if (!confirmPassword) errors.confirmPassword = "Please confirm your password.";
  else if (password !== confirmPassword) errors.confirmPassword = "Passwords do not match.";

  return errors;
};

export const getPasswordStrength = (password) => {
  let score = 0;

  if (password.length >= 8) score += 1;
  if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score += 1;
  if (/\d/.test(password)) score += 1;
  if (/[^A-Za-z0-9]/.test(password)) score += 1;

  if (score <= 1) return { label: "Weak", level: "weak" };
  if (score <= 3) return { label: "Medium", level: "medium" };
  return { label: "Strong", level: "strong" };
};

export const getApiErrorMessage = (error, fallbackMessage) => {
  const detail = error.response?.data?.detail;

  if (Array.isArray(detail)) return detail.map((item) => item.msg).join(" ");
  return detail || error.message || fallbackMessage;
};
