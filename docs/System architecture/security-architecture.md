# Security Architecture

## Purpose

This document defines the security architecture of the Student Study Assistant platform.

The objective is to protect:

* user accounts,
* uploaded study materials,
* chat history,
* API endpoints,
* AI interactions,
* application infrastructure.

The security architecture is designed to provide production-quality security practices while remaining appropriate for an MVP developed as a modular monolith.

---

# Security Principles

## Principle 1

Every request must be authenticated unless explicitly marked as public.

---

## Principle 2

Every resource is owned by exactly one user.

Authorization must be enforced on every request.

---

## Principle 3

Least privilege should be applied throughout the system.

Every component should receive only the permissions required to perform its responsibilities.

---

## Principle 4

Uploaded documents are treated as untrusted input.

No uploaded content may override application instructions or system prompts.

---

## Principle 5

Sensitive information must never be stored or logged in plaintext.

---

# Security Objectives

The platform aims to provide:

* Confidentiality
* Integrity
* Availability
* Privacy
* Secure AI interactions

---

# Authentication

## Supported Methods

* Email and Password
* Google OAuth

---

## Password Storage

Passwords shall never be stored in plaintext.

The application shall store only secure password hashes.

Recommended algorithm:

```text
Argon2id
```

---

## JWT Authentication

Authentication uses:

```text
Access Token
Refresh Token
```

Access tokens authenticate API requests.

Refresh tokens obtain new access tokens without requiring users to log in again.

---

## Session Security

The backend validates:

* token signature
* expiration
* issuer
* user existence
* account status

Expired or invalid tokens shall immediately be rejected.

---

# Authorization

Authorization is ownership-based.

Every protected resource belongs to exactly one user.

Examples:

* Workspace
* Document
* Chat Session
* User Preferences

Ownership is validated on every request.

Example:

```text
Request

↓

Authenticate User

↓

Load Resource

↓

Verify Ownership

↓

Allow or Deny
```

Users shall never be able to access resources belonging to another user.

---

# API Security

## HTTPS

Production deployments shall use HTTPS for all communications.

Development environments may use HTTP locally.

---

## CORS

Development:

Allow localhost frontend.

Production:

Only explicitly configured frontend domains shall be permitted.

Wildcard origins shall not be used in production.

---

## HTTP Headers

The application should support standard security headers.

Examples:

* X-Content-Type-Options
* Referrer-Policy
* X-Frame-Options

Content Security Policy may be introduced in future versions.

---

# Rate Limiting

The MVP uses lightweight rate limiting for sensitive endpoints.

| Endpoint        | Limit                    |
| --------------- | ------------------------ |
| Login           | 5 requests/minute/IP     |
| Registration    | 3 requests/minute/IP     |
| Password Reset  | 3 requests/15 minutes/IP |
| Document Upload | 10 uploads/minute/user   |
| Chat            | 30 requests/minute/user  |

General read endpoints are not rate limited during the MVP.

---

# Input Validation

Every request must be validated before processing.

Validation includes:

* schema validation
* data type validation
* required fields
* maximum lengths
* allowed values

Validation failures shall return structured error responses.

---

# File Upload Security

Supported file types:

* PDF
* PNG
* JPG

Validation pipeline:

```text
Authentication
        ↓
Workspace Ownership
        ↓
Extension Validation
        ↓
MIME Type Validation
        ↓
Maximum File Size
        ↓
Store File
        ↓
Background Processing
```

Future improvements:

* Virus scanning
* Malware detection
* File signature validation

---

# Secure File Storage

Uploaded files are stored outside publicly accessible directories.

Users access documents only through authenticated API endpoints.

Storage paths are generated internally.

User-supplied file paths are never trusted.

---

# Database Security

The application uses PostgreSQL as the primary database.

Security practices include:

* SQLAlchemy ORM
* parameterized queries
* UUID primary keys
* ownership validation

Raw SQL should be avoided whenever possible.

---

# Secret Management

Sensitive configuration values must never be hardcoded.

Examples:

* JWT secrets
* OAuth credentials
* API keys
* Database passwords

Secrets are loaded from environment variables.

Example:

```text
.env

↓

Configuration

↓

Application
```

---

# Logging and Auditing

Application logs should support debugging while protecting user privacy.

The system shall never log:

* passwords
* JWTs
* refresh tokens
* OAuth tokens
* API keys
* Authorization headers

Operational logs may include:

* request ID
* endpoint
* response status
* processing duration
* background job status
* errors

---

# AI Security

## Prompt Injection

Uploaded documents are treated as untrusted content.

Retrieved context is used as reference material only.

Documents must never override:

* system prompts
* application instructions
* safety rules

---

## Workspace Isolation

Every retrieval request filters by:

* user_id
* workspace_id

The retrieval pipeline must never access another user's embeddings.

---

## Hallucination Mitigation

When relevant documents exist:

* prioritize retrieved information
* provide citations

When retrieval fails:

* clearly indicate that generic knowledge is being used

---

# Privacy

Users retain ownership of:

* uploaded documents
* chat history
* preferences

The platform shall not expose user data to other users.

Data collection shall be limited to information required for platform functionality.

---

# Encryption

## In Transit

HTTPS protects all production communication.

---

## At Rest

Application data relies on operating system or infrastructure disk encryption.

Application-level file encryption is outside MVP scope.

---

# Background Job Security

Background workers process only trusted internal jobs.

Workers validate:

* document ownership
* workspace association
* processing status

Cancelled documents must not continue processing.

---

# Security Monitoring

The application should monitor:

* failed login attempts
* authorization failures
* upload failures
* background job failures
* unexpected application errors

---

# Threat Model

| Threat                 | Mitigation                                   |
| ---------------------- | -------------------------------------------- |
| Unauthorized Access    | Authentication and ownership validation      |
| SQL Injection          | SQLAlchemy ORM and parameterized queries     |
| Path Traversal         | Internal storage path generation             |
| Malicious File Upload  | File type, MIME type and size validation     |
| Prompt Injection       | Treat retrieved documents as untrusted input |
| Brute Force Login      | Rate limiting                                |
| Token Theft            | HTTPS and short-lived access tokens          |
| Cross-User Data Access | User and workspace filtering                 |
| Sensitive Data Leakage | Secure logging practices                     |

---

# Future Security Enhancements

Potential improvements include:

* Multi-factor authentication
* Email verification
* Virus scanning
* Security event monitoring
* Audit log dashboard
* Content Security Policy
* Automated secret rotation
* Object storage encryption
* Web Application Firewall
* Intrusion detection

---

# Design Rationale

The MVP prioritizes practical, production-oriented security while avoiding unnecessary operational complexity.

The architecture focuses on:

* strong authentication,
* strict authorization,
* secure document handling,
* privacy protection,
* secure AI interactions,
* future extensibility.

The design intentionally follows the principle that every user resource is isolated by ownership, every AI interaction is grounded within the user's workspace, and every uploaded document is treated as untrusted input.

---

# Status

Accepted.

This document should be reviewed whenever:

* authentication mechanisms change,
* deployment models change,
* external providers are added,
* collaboration features are introduced,
* new security requirements emerge.
