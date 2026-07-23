import { useState } from "react";

import "./AuthLayout.css";

function VisibilityIcon({ isVisible }) {
  return isVisible ? (
    <svg aria-hidden="true" viewBox="0 0 24 24">
      <path d="M3 3l18 18M10.6 10.7a2 2 0 0 0 2.7 2.7M9.9 4.2A10.9 10.9 0 0 1 12 4c5.5 0 9.4 5.3 10 8-.2.8-.7 1.9-1.5 3M6.6 6.7C4.2 8.3 2.5 10.8 2 12c.6 2.7 4.5 8 10 8 1.2 0 2.4-.3 3.4-.7" />
    </svg>
  ) : (
    <svg aria-hidden="true" viewBox="0 0 24 24">
      <path d="M2 12s3.6-8 10-8 10 8 10 8-3.6 8-10 8S2 12 2 12Z" />
      <circle cx="12" cy="12" r="3" />
    </svg>
  );
}

export function PasswordInput({ id, label, value, onChange, error, autoComplete, placeholder, hint }) {
  const [isVisible, setIsVisible] = useState(false);
  const errorId = `${id}-error`;

  return (
    <div className="auth-field">
      <label htmlFor={id}>{label}</label>
      <div className="password-control">
        <input
          id={id}
          name={id}
          type={isVisible ? "text" : "password"}
          autoComplete={autoComplete}
          value={value}
          onChange={onChange}
          aria-invalid={Boolean(error)}
          aria-describedby={error ? errorId : undefined}
          placeholder={placeholder}
        />
        <button
          className="password-toggle"
          type="button"
          onClick={() => setIsVisible((currentValue) => !currentValue)}
          aria-label={isVisible ? `Hide ${label.toLowerCase()}` : `Show ${label.toLowerCase()}`}
          aria-pressed={isVisible}
        >
          <VisibilityIcon isVisible={isVisible} />
        </button>
      </div>
      {error && <p id={errorId} className="field-error">{error}</p>}
      {hint}
    </div>
  );
}

function AuthLayout({ eyebrow, title, description, children, footer, titleId }) {
  return (
    <main className="auth-page">
      <section className="auth-card" aria-labelledby={titleId}>
        <div className="auth-brand" aria-hidden="true">GA</div>
        <p className="auth-eyebrow">{eyebrow}</p>
        <h1 id={titleId}>{title}</h1>
        <p className="auth-subtitle">{description}</p>
        {children}
        <div className="auth-footer">{footer}</div>
      </section>
    </main>
  );
}

export default AuthLayout;
