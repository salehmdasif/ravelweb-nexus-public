# Security Overview: Ravelweb Nexus

This document describes the security model at a high level. Implementation details are
not included in this public version.

---

## Authentication

### Web Application

- Session-based authentication using Flask's signed, encrypted server-side session cookies.
- Passwords are hashed using Werkzeug's PBKDF2 implementation with a per-user salt.
- Google OAuth 2.0 is available as an alternative login method via Authlib.
- Email verification is required before account access is granted.
- OTP-based password recovery sends a time-limited code to the registered email.
- Failed login attempts trigger progressive lockout.
- A screen-lock feature allows users to lock their session without logging out.

### Mobile API

- JWT Bearer tokens with short expiry (30 minutes by default).
- Refresh token rotation: a new refresh token is issued on each refresh.
- Token blacklist via Redis allows immediate invalidation on logout or forced revocation.

### SaaS Admin Panel

- Password authentication plus TOTP two-factor authentication (TOTP via pyotp).
- Standard TOTP apps are supported (Google Authenticator, Authy, etc.).
- TOTP setup is a one-time flow during admin provisioning.

---

## Authorization

### Role-Based Access Control (RBAC)

Four roles enforce what each user can do:

| Role | Access Level |
|------|-------------|
| Superadmin | Full platform control |
| Admin | Full tenant access |
| Manager | Most operations; no settings, no system config |
| Salesman | Sales and customer operations only |

Role is stored in the encrypted session and checked per-route via Python decorators:

```python
@role_required('Admin', 'Manager')
def some_route():
    ...
```

The `superadmin_session_required` decorator separately gates all SaaS admin panel routes.

### Tenant Isolation

The tenant middleware resolves the correct database before any route runs. Routes call
`get_db()` which returns a connection to the correct tenant database for the current
session -- it is not possible to query another tenant's database by accident from
normal application code.

---

## Data Isolation

Each tenant's business data lives in a separate PostgreSQL database. The database name
is stored in the session after login and verified on every request. There is no
shared-schema or row-level tenant isolation -- isolation is enforced at the database level.

---

## Session Revocation

Active sessions can be invalidated without waiting for cookie expiry:

- When a superadmin deactivates a user or revokes a tenant, a signal is written to Redis.
- The tenant middleware checks this signal on every authenticated request.
- If a revocation signal is found, the session is cleared and the user is redirected to login.

This provides near-instant revocation without a database query on every request.

---

## CSRF Protection

Flask-WTF provides CSRF protection on all HTML form submissions. The CSRF token is
embedded in every form and verified server-side. CSRF protection is explicitly disabled
only for the Mobile API Blueprint, which uses JWT authentication instead.

---

## Rate Limiting

Flask-Limiter applies rate limits to sensitive endpoints using Redis as the shared counter
store. Rate limits are applied to:

- Login endpoint (brute-force protection)
- Registration endpoint (spam prevention)
- OTP request endpoint (abuse prevention)
- Mobile API auth endpoints

Limits are shared across all Gunicorn workers via Redis, so rate limiting works correctly
under multi-process deployment.

---

## API Key Security

LLM provider API keys entered by the superadmin are encrypted at rest using Fernet
symmetric encryption. The encryption key is derived from the application's `SECRET_KEY`
via SHA-256. Keys are decrypted only at the time of an API call and are never logged
or exposed in responses.

---

## License Security

The license system uses two independent validation layers:

1. **JWT signature verification:** The license token is signed with a shared secret.
   An invalid signature means the token was not issued by this platform.

2. **Database status check:** Even a valid JWT is rejected if the main database shows
   the license as `revoked` or `suspended`. This allows instant revocation by the
   operator without waiting for token expiry.

---

## Input Validation

- All form inputs are validated server-side before any database operation.
- Parameterized queries are used exclusively. No string interpolation in SQL.
- File uploads are validated for type and size before storage.

---

## Error Handling

- 500 errors do not expose stack traces to the user. A generic error page is shown.
- 500 errors trigger a non-blocking email alert to the operator if SMTP is configured.
- JSON error responses are returned for API paths; HTML for browser paths.

---

## Production Hardening

- `SESSION_COOKIE_SECURE = True` in production (HTTPS-only cookie transmission).
- `SESSION_COOKIE_HTTPONLY = True` (JavaScript cannot read the session cookie).
- The application refuses to start if `FLASK_DEBUG` is enabled in production mode.
- Default placeholder secrets trigger a startup error in production mode.
- The application is deployed behind Nginx which handles SSL termination and sets
  appropriate security headers.

---

## Compliance Considerations

- User passwords are never stored in plaintext.
- Sensitive configuration (API keys, SMTP passwords) are stored encrypted or as
  environment variables, never in the codebase.
- The audit log provides a record of all write actions for accountability.
- Tenant offboarding permanently drops the database, satisfying data deletion requirements.
