# API Design

## Purpose

This document defines the API contract for the Student Study Assistant platform.

The API serves as the communication layer between:

* Frontend (React)
* Backend (FastAPI)
* External clients (future)

The objectives are:

* simplicity,
* consistency,
* maintainability,
* future extensibility,
* production-ready design.

---

# API Design Principles

## Principle 1

REST-first architecture.

---

## Principle 2

All endpoints are versioned.

```text
/api/v1
```

---

## Principle 3

Every endpoint requires authentication unless explicitly marked public.

---

## Principle 4

All resources are user scoped.

A user can only access their own:

* workspaces
* documents
* chats
* preferences

---

## Principle 5

Long-running operations are asynchronous.

Examples:

* document processing
* indexing

---

## Principle 6

Streaming responses should use Server-Sent Events (SSE).

---

# Base URL

```text
/api/v1
```

---

# Authentication Strategy

Authentication mechanisms:

* Email + Password
* Google OAuth

Authentication method:

```text
JWT Access Token
JWT Refresh Token
```

Authorization:

```text
Bearer Token
```

Example:

```http
Authorization: Bearer <token>
```

---

# API Versioning Strategy

```text
/api/v1/...
```

Future:

```text
/api/v2/...
```

---

# Standard Success Response

```json
{
  "success": true,
  "data": {},
  "message": null
}
```

---

# Standard Error Response

```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Workspace not found"
  }
}
```

---

```text
API response strategy: Resource endpoints return their resource representation directly. HTTP status codes communicate request outcome. Errors use structured error responses. A universal success/data/message envelope is not currently used because the application does not require the additional abstraction or response metadata. This decision can be revisited if API complexity, pagination metadata, client requirements, or external consumers justify it.
```

---

# Pagination Strategy

Page-based pagination.

Request:

```http
GET /workspaces?page=1&page_size=20
```

Response:

```json
{
  "items": [],
  "page": 1,
  "page_size": 20,
  "total": 100,
  "has_next": true
}
```

---

# HTTP Status Codes

| Status | Meaning               |
| ------ | --------------------- |
| 200    | Success               |
| 201    | Created               |
| 202    | Accepted              |
| 204    | Deleted               |
| 400    | Bad Request           |
| 401    | Unauthorized          |
| 403    | Forbidden             |
| 404    | Not Found             |
| 409    | Conflict              |
| 413    | File Too Large        |
| 422    | Validation Error      |
| 429    | Too Many Requests     |
| 500    | Internal Server Error |

---

# Authentication Endpoints

## Register

```http
POST /api/v1/auth/register
```

---

## Login

```http
POST /api/v1/auth/login
```

---

## Refresh Token

```http
POST /api/v1/auth/refresh
```

---

## Logout

```http
POST /api/v1/auth/logout
```

---

## Forgot Password

```http
POST /api/v1/auth/forgot-password
```

---

## Reset Password

```http
POST /api/v1/auth/reset-password
```

---

## Google Login

```http
GET /api/v1/auth/google/login
GET /api/v1/auth/google/callback
```

---

## Get Current User

```http
GET /api/v1/users/me
```

---

# Workspace Endpoints

## Create Workspace

```http
POST /api/v1/workspaces
```

---

## List Workspaces

```http
GET /api/v1/workspaces
```

---

## Get Workspace

```http
GET /api/v1/workspaces/{workspace_id}
```

---

## Update Workspace

```http
PATCH /api/v1/workspaces/{workspace_id}
```

---

## Delete Workspace

```http
DELETE /api/v1/workspaces/{workspace_id}
```

Returns:

```http
204 No Content
```

---

# Workspace Preferences

## Get Preferences

```http
GET /api/v1/workspaces/{workspace_id}/preferences
```

---

## Update Preferences

```http
PATCH /api/v1/workspaces/{workspace_id}/preferences
```

---

# Document Endpoints

## Upload Document

```http
POST /api/v1/workspaces/{workspace_id}/documents
```

Content Type:

```text
multipart/form-data
```

---

## List Documents

```http
GET /api/v1/workspaces/{workspace_id}/documents
```

---

## Get Document

```http
GET /api/v1/documents/{document_id}
```

---

## Delete Document

```http
DELETE /api/v1/documents/{document_id}
```

Returns:

```http
204 No Content
```

---

## Get Processing Status

```http
GET /api/v1/documents/{document_id}/status
```

---

## Retry Processing

```http
POST /api/v1/documents/{document_id}/retry
```

---

# Job Endpoints

## Get Processing Job

```http
GET /api/v1/jobs/{job_id}
```

---

## List Document Jobs

```http
GET /api/v1/documents/{document_id}/jobs
```

---

# Search Endpoints

## Semantic Search

```http
POST /api/v1/workspaces/{workspace_id}/search
```

Request:

```json
{
  "query": "Explain normalization",
  "top_k": 5
}
```

---

Response:

```json
{
  "results": []
}
```

---

# Chat Session Endpoints

## Create Session

```http
POST /api/v1/chat/sessions
```

---

## List Sessions

```http
GET /api/v1/workspaces/{workspace_id}/chat/sessions
```

---

## Get Session

```http
GET /api/v1/chat/sessions/{session_id}
```

---

## Delete Session

```http
DELETE /api/v1/chat/sessions/{session_id}
```

Returns:

```http
204 No Content
```

---

# Message Endpoints

## Send Message

```http
POST /api/v1/chat/sessions/{session_id}/messages
```

---

## Stream Message (SSE)

```http
POST /api/v1/chat/sessions/{session_id}/messages/stream
```

Response Type:

```text
text/event-stream
```

---

## List Messages

```http
GET /api/v1/chat/sessions/{session_id}/messages
```

---

# User Preference Endpoints

## Get Preferences

```http
GET /api/v1/users/me/preferences
```

---

## Update Preferences

```http
PATCH /api/v1/users/me/preferences
```

---

# Health Endpoints

## Liveness Check

```http
GET /api/v1/health/live
```

---

## Readiness Check

```http
GET /api/v1/health/ready
```

---

## Health Details

```http
GET /api/v1/health
```

---

# Document Upload Flow

```text
Upload Document
        ↓
Create Document Record
        ↓
Create Processing Job
        ↓
Return 202 Accepted
        ↓
Background Processing
        ↓
Status Polling
        ↓
Ready
```

---

# Chat Flow

```text
User Question
        ↓
Retrieve Context
        ↓
Generate Response
        ↓
Store Messages
        ↓
Store Citations
        ↓
Return Response
```

---

# Streaming Flow

```text
User Message
        ↓
Retrieve Context
        ↓
LLM Generation
        ↓
SSE Token Stream
        ↓
Store Final Message
```

---

# Authorization Rules

Users can only access resources they own.

Ownership checks must exist for:

* workspace_id
* document_id
* chat_session_id
* message_id
* job_id

---

# Rate Limiting Strategy

MVP:

No strict rate limiting.

Future:

* authentication endpoints
* chat endpoints
* upload endpoints

---

# Future API Extensions

```text
/api/v1/quizzes
/api/v1/flashcards
/api/v1/analytics
/api/v1/study-plans
/api/v1/cross-workspace-search
/api/v1/collaboration
```

---

# Design Rationale

## Why REST?

* Simple
* Familiar
* Easy to document
* Good portfolio value

---

## Why SSE instead of WebSockets?

* Simpler implementation
* Excellent for AI streaming
* Lower complexity
* Sufficient for MVP

---

## Why Polling for Processing Status?

* Easier to implement
* Adequate for low traffic
* Avoids unnecessary real-time infrastructure

---

## Why Explicit Chat Sessions?

* Better conversation management
* Easier persistence
* More extensible

---

# Status

Accepted.

This document should be revisited whenever:

* new clients are added,
* collaboration is introduced,
* cross-workspace features are added,
* real-time requirements change,
* API versioning changes.
