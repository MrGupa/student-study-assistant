# Authentication Design

## Purpose

This document defines the authentication and authorization architecture for the Student Study Assistant platform.

It specifies:

* Identity management
* Authentication mechanisms
* Authorization model
* JWT lifecycle
* Session management
* Password security
* OAuth integration
* Security considerations

The objective is to provide a secure, maintainable, and extensible authentication system that supports the MVP while allowing future enhancements with minimal architectural changes.

---

# Scope

This document covers:

* User authentication
* User authorization
* JWT management
* Refresh token strategy
* Password management
* Google OAuth integration
* Authentication flows
* Security decisions

It does **not** cover:

* User profile management
* Permissions beyond ownership-based authorization
* Future administrative roles

---

# Design Goals

The authentication system should:

1. Support multiple authentication methods.
2. Keep authentication independent from business logic.
3. Enforce ownership-based authorization.
4. Minimize security risks.
5. Support future authentication providers.
6. Remain compatible with future cloud and self-hosted deployments.

---

# Guiding Principles

## Principle 1 — Separate Authentication and Authorization

Authentication answers:

> Who is the user?

Authorization answers:

> Can this user perform this action?

These responsibilities should remain independent.

---

## Principle 2 — Provider-Agnostic Identity

Users may authenticate using:

* Email and Password
* Google OAuth

Regardless of the login method, both resolve to the same internal **User** entity.

Future providers should integrate without requiring changes to business logic.

---

## Principle 3 — Stateless Backend Authentication

The backend remains stateless.

Authentication is performed using JWTs.

No server-side session storage is required during the MVP.

---

## Principle 4 — Ownership-Based Authorization

The MVP does not implement user roles.

Authorization is based entirely on resource ownership.

Examples:

* User owns Workspace
* Workspace owns Documents
* Workspace owns Chat Sessions

Every protected request ultimately verifies ownership.

---

# Authentication Methods

## Supported

### Email + Password

Capabilities:

* Registration
* Login
* Password Reset

---

### Google OAuth 2.0

Capabilities:

* Sign in with Google
* Automatic account creation
* Returning user login

---

## Future

The architecture should support additional providers including:

* GitHub
* Microsoft
* Apple

without modifying business logic.

---

# High-Level Authentication Architecture

```text
                User
               /    \
              /      \
 Email/Password   Google OAuth
         \            /
          \          /
     Authentication Service
              |
         JWT Service
              |
      Protected Resources
```

---

# Authentication Components

## Frontend

Responsibilities:

* Login UI
* Registration UI
* OAuth initiation
* Access token management
* Automatic token refresh
* Logout

---

## Authentication API

Responsibilities:

* User registration
* Login
* Refresh token
* Password reset
* Google OAuth callback

---

## Authentication Service

Responsibilities:

* Validate credentials
* Create users
* Generate JWTs
* Verify identities

---

## Password Service

Responsibilities:

* Hash passwords
* Verify passwords

Algorithm:

**Argon2id** via `pwdlib`

---

## JWT Service

Responsibilities:

* Create access tokens
* Create refresh tokens
* Validate tokens
* Extract user identity

---

## OAuth Service

Responsibilities:

* Google OAuth flow
* Identity verification
* User creation
* Existing account lookup

---

## Current User Dependency

FastAPI dependency responsible for:

* Reading JWT
* Validating JWT
* Loading authenticated user
* Rejecting invalid requests

Business services should never parse JWTs directly.

---

# Token Strategy

## Access Token

Purpose:

Authenticate API requests.

Characteristics:

* JWT
* Short-lived
* Stored only in React application memory
* Included in Authorization header

Recommended Lifetime:

**15 minutes**

---

## Refresh Token

Purpose:

Generate new access tokens.

Characteristics:

* JWT
* Long-lived
* Stored in an HttpOnly Secure Cookie
* Automatically sent by the browser
* Not accessible to JavaScript

Recommended Lifetime:

**30 days**

---

# Token Storage Strategy

## Access Token

Storage:

React application memory only.

Reasons:

* Reduced XSS exposure
* Automatically removed when the browser tab is closed
* Simpler than encrypted browser storage

---

## Refresh Token

Storage:

HttpOnly Secure Cookie.

Reasons:

* Not accessible through JavaScript
* Better protection against XSS
* Long-lived authentication

---

# Authentication Flow

## User Registration

```text
User
    ↓
Submit Registration
    ↓
Validate Input
    ↓
Hash Password
    ↓
Create User
    ↓
Create Default Preferences
    ↓
Generate JWTs
    ↓
Return Access Token
Set Refresh Cookie
```

---

## Email Login

```text
User
    ↓
Submit Credentials
    ↓
Verify Password
    ↓
Generate JWTs
    ↓
Return Access Token
Set Refresh Cookie
```

---

## Google OAuth Login

```text
User
    ↓
Google OAuth
    ↓
Authorization Code
    ↓
Backend Callback
    ↓
Verify Google Identity
    ↓
Find or Create User
    ↓
Generate JWTs
    ↓
Return Access Token
Set Refresh Cookie
```

---

## Token Refresh Flow

```text
Access Token Expires
        ↓
Frontend Calls
/api/v1/auth/refresh
        ↓
Refresh Token Cookie Sent Automatically
        ↓
Validate Refresh Token
        ↓
Generate New Access Token
        ↓
Return New Access Token
```

---

# Logout Flow

```text
User Clicks Logout
        ↓
Frontend Calls Logout Endpoint
        ↓
Backend Clears Refresh Cookie
        ↓
Frontend Removes Access Token
        ↓
User Becomes Unauthenticated
```

---

# Authorization Model

Every protected request follows the same process.

```text
Incoming Request
        ↓
Validate JWT
        ↓
Load Current User
        ↓
Load Requested Resource
        ↓
Verify Ownership
        ↓
Allow or Reject Request
```

---

## Ownership Rules

Users may access only:

* Their own workspaces
* Their own documents
* Their own chat sessions
* Their own preferences
* Their own processing jobs

---

# FastAPI Dependency Chain

```text
Request
    ↓
JWT Validation
    ↓
Current User
    ↓
Ownership Check
    ↓
Endpoint Logic
```

Authentication logic should remain outside business services.

---

# Password Security

Passwords are never stored in plaintext.

Requirements:

* Use Argon2id via `pwdlib`
* Never log passwords
* Never expose password hashes
* Always hash before persistence

---

# JWT Claims

Access Token should include:

```text
sub        -> User ID
email      -> User Email
type       -> access
exp        -> Expiration
iat        -> Issued At
```

Refresh Token:

```text
sub
type = refresh
exp
iat
```

No application-specific permissions should be stored inside JWTs.

Authorization is determined using database ownership checks.

---

# Protected Endpoints

Require authentication:

* Workspace APIs
* Document APIs
* Search APIs
* Chat APIs
* Preferences APIs
* Job APIs

---

# Public Endpoints

No authentication required:

* Register
* Login
* Refresh Token
* Forgot Password
* Reset Password
* Google OAuth Callback
* Health Endpoints

---

# Password Reset Flow

```text
Forgot Password
        ↓
Generate Reset Token
        ↓
Send Email
        ↓
User Opens Link
        ↓
Validate Token
        ↓
Set New Password
```

---

# Error Handling

| Situation             | Response         |
| --------------------- | ---------------- |
| Invalid credentials   | 401 Unauthorized |
| Missing token         | 401 Unauthorized |
| Expired access token  | 401 Unauthorized |
| Invalid refresh token | 401 Unauthorized |
| Disabled account      | 403 Forbidden    |
| Resource not owned    | 403 Forbidden    |

---

# Security Considerations

## Password Security

* Argon2id hashing
* No plaintext passwords
* No password logging

---

## Token Security

* HTTPS required in production
* Short-lived access tokens
* HttpOnly Secure refresh cookies

---

## OAuth Security

* Verify Google-issued identity tokens
* Validate issuer
* Validate audience
* Never trust client-provided profile information

---

## Authorization Security

Every protected endpoint must perform ownership validation.

Never trust identifiers supplied by the client.

---

## Brute Force Protection

Future enhancement:

* Login rate limiting
* Temporary account lockout
* Progressive delays after repeated failures

---

## CSRF Considerations

Because refresh tokens are stored in HttpOnly cookies, the refresh endpoint should include CSRF protection before production deployment.

For the MVP, the application will:

* use SameSite cookie settings,
* restrict allowed origins through CORS,
* expose only the refresh endpoint to cookie-based authentication.

Additional CSRF defenses may be added in future releases.

---

# Future Enhancements

* Email verification
* Refresh token rotation
* Server-side session revocation
* Multi-device session management
* Two-Factor Authentication (2FA)
* Passkeys (WebAuthn)
* Additional OAuth providers
* Administrative roles

---

# Design Rationale

| Decision                         | Rationale                                     |
| -------------------------------- | --------------------------------------------- |
| JWT Authentication               | Stateless API authentication                  |
| Access Token in Memory           | Reduces XSS exposure                          |
| Refresh Token in HttpOnly Cookie | Better security for long-lived authentication |
| Ownership-Based Authorization    | Matches the domain model and MVP scope        |
| Email + Google OAuth             | Covers most expected user login preferences   |
| Argon2id Password Hashing        | Modern and secure password hashing            |
| Provider Abstraction             | Simplifies adding future identity providers   |

---

# Implementation Notes

This document defines the intended authentication architecture for the MVP.

Implementation should follow this design unless significant technical constraints are discovered during development.

If implementation changes the authentication architecture, this document should be updated to remain the project's source of truth.

---

# Status

**Accepted**

This document should be reviewed whenever:

* authentication providers change,
* session management changes,
* authorization rules evolve,
* new security requirements are introduced.
