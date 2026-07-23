import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import AuthLayout, { PasswordInput } from "../../layouts/AuthLayout";
import { registerUser } from "../../services/authService";
import {
  getApiErrorMessage,
  getPasswordStrength,
  validateRegistrationForm,
} from "../../utils/authValidation";

const initialForm = { username: "", email: "", password: "", confirmPassword: "" };

function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState(initialForm);
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const passwordStrength = getPasswordStrength(form.password);

  const validate = () => {
    const nextErrors = validateRegistrationForm(form);
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
      await registerUser({
        username: form.username.trim(),
        email: form.email.trim(),
        password: form.password,
      });

      navigate("/", {
        replace: true,
        state: { successMessage: "Account created successfully. You can now sign in." },
      });
    } catch (error) {
      setServerError(getApiErrorMessage(error, "Unable to create your account. Please try again."));
    } finally {
      setIsSubmitting(false);
    }
  };

  const passwordHint = form.password ? (
    <div className="password-strength" aria-live="polite">
      <div className={`strength-bar ${passwordStrength.level}`} aria-hidden="true">
        <span />
        <span />
        <span />
      </div>
      <span>Password strength: {passwordStrength.label}</span>
    </div>
  ) : null;

  return (
    <AuthLayout
      eyebrow="GeoAsset Tracker"
      title="Create your account"
      titleId="register-title"
      description="Set up your workspace and start tracking your geospatial assets."
      footer={(
        <>
          Already have an account? <Link to="/">Login</Link>
        </>
      )}
    >
      <form className="auth-form" onSubmit={handleSubmit} noValidate>
        {serverError && <div className="form-alert" role="alert">{serverError}</div>}

        <div className="auth-field">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            name="username"
            type="text"
            autoComplete="username"
            value={form.username}
            onChange={handleChange}
            aria-invalid={Boolean(errors.username)}
            aria-describedby={errors.username ? "username-error" : undefined}
            placeholder="Choose a username"
          />
          {errors.username && <p id="username-error" className="field-error">{errors.username}</p>}
        </div>

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
          autoComplete="new-password"
          value={form.password}
          onChange={handleChange}
          error={errors.password}
          placeholder="Create a password"
          hint={passwordHint}
        />

        <PasswordInput
          id="confirmPassword"
          label="Confirm password"
          autoComplete="new-password"
          value={form.confirmPassword}
          onChange={handleChange}
          error={errors.confirmPassword}
          placeholder="Re-enter your password"
        />

        <button className="auth-submit" type="submit" disabled={isSubmitting}>
          {isSubmitting && <span className="button-spinner" aria-hidden="true" />}
          {isSubmitting ? "Creating account..." : "Create account"}
        </button>
      </form>
    </AuthLayout>
  );
}

export default Register;
