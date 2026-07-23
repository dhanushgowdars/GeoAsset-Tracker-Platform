import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

import AuthLayout, { PasswordInput } from "../../layouts/AuthLayout";
import { loginUser } from "../../services/authService";
import { getApiErrorMessage, validateLoginForm } from "../../utils/authValidation";
import { saveToken } from "../../utils/storage";

const initialForm = { email: "", password: "" };

function Login() {
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState(initialForm);
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validate = () => {
    const nextErrors = validateLoginForm(form);
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
      setServerError(getApiErrorMessage(error, "Unable to sign in. Please try again."));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <AuthLayout
      eyebrow="GeoAsset Tracker"
      title="Welcome back"
      titleId="login-title"
      description="Sign in to manage your geospatial assets."
      footer={(
        <>
          Don't have an account? <Link to="/register">Register</Link>
        </>
      )}
    >
      <form className="auth-form" onSubmit={handleSubmit} noValidate>
        {location.state?.successMessage && (
          <div className="form-success" role="status">{location.state.successMessage}</div>
        )}
        {serverError && <div className="form-alert" role="alert">{serverError}</div>}

        <div className="auth-field">
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
        </div>

        <PasswordInput
          id="password"
          label="Password"
          autoComplete="current-password"
          value={form.password}
          onChange={handleChange}
          error={errors.password}
          placeholder="Enter your password"
        />

        <button className="auth-submit" type="submit" disabled={isSubmitting}>
          {isSubmitting && <span className="button-spinner" aria-hidden="true" />}
          {isSubmitting ? "Signing in..." : "Sign in"}
        </button>
      </form>
    </AuthLayout>
  );
}

export default Login;
