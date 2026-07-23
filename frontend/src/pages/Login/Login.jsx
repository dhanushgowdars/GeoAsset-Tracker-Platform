import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";

import { loginUser } from "../../services/authService";
import { getToken, saveToken } from "../../utils/storage";
import "./Login.css";

const initialForm = { email: "", password: "" };

function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState(initialForm);
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (getToken()) return <Navigate to="/dashboard" replace />;

  const validate = () => {
    const nextErrors = {};

    if (!form.email.trim()) nextErrors.email = "Email is required.";
    else if (!/^\S+@\S+\.\S+$/.test(form.email)) nextErrors.email = "Enter a valid email address.";

    if (!form.password) nextErrors.password = "Password is required.";
    else if (form.password.length < 8) nextErrors.password = "Password must be at least 8 characters.";

    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const handleChange = ({ target: { name, value } }) => {
    setForm((currentForm) => ({ ...currentForm, [name]: value }));
    setErrors((currentErrors) => ({ ...currentErrors, [name]: "" }));
    setServerError("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!validate()) return;

    setIsSubmitting(true);
    setServerError("");

    try {
      const { access_token: accessToken } = await loginUser({
        email: form.email.trim(),
        password: form.password,
      });

      if (!accessToken) throw new Error("The server did not return an access token.");

      saveToken(accessToken);
      navigate("/dashboard", { replace: true });
    } catch (error) {
      const detail = error.response?.data?.detail;
      setServerError(
        Array.isArray(detail)
          ? detail.map((item) => item.msg).join(" ")
          : detail || error.message || "Unable to sign in. Please try again.",
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="auth-page">
      <section className="auth-card" aria-labelledby="login-title">
        <div className="auth-brand" aria-hidden="true">GA</div>
        <p className="auth-eyebrow">GeoAsset Tracker</p>
        <h1 id="login-title">Welcome back</h1>
        <p className="auth-subtitle">Sign in to manage your geospatial assets.</p>

        <form className="auth-form" onSubmit={handleSubmit} noValidate>
          {serverError && <div className="form-alert" role="alert">{serverError}</div>}

          <label htmlFor="email">Email address</label>
          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            value={form.email}
            onChange={handleChange}
            aria-invalid={Boolean(errors.email)}
            aria-describedby={errors.email ? "email-error" : undefined}
            placeholder="you@example.com"
          />
          {errors.email && <p id="email-error" className="field-error">{errors.email}</p>}

          <label htmlFor="password">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            value={form.password}
            onChange={handleChange}
            aria-invalid={Boolean(errors.password)}
            aria-describedby={errors.password ? "password-error" : undefined}
            placeholder="Enter your password"
          />
          {errors.password && <p id="password-error" className="field-error">{errors.password}</p>}

          <button className="auth-submit" type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Signing in…" : "Sign in"}
          </button>
        </form>
      </section>
    </main>
  );
}

export default Login;
