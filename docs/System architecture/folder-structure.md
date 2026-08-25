# Folder Structure

## Purpose

This document defines the directory structure of the Student Study Assistant project.

The folder structure translates the system architecture into an organized, maintainable codebase.

The goals are:

* feature-based organization,
* clear separation of concerns,
* modular development,
* scalability,
* maintainability,
* consistency across the project.

---

# Project Structure

```text
student-study-assistant/

├── backend/
├── frontend/
├── docker/
├── docs/
├── scripts/
├── .github/
│   └── workflows/
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
└── LICENSE
```

---

# Root Directory

## backend/

Contains the FastAPI application and all backend services.

---

## frontend/

Contains the React + TypeScript application.

---

## docker/

Dockerfiles and Docker-related configuration.

---

## docs/

Architecture documentation.

Includes:

* Requirements
* ADR Summary
* Database Design
* API Design
* RAG Architecture
* Authentication Design
* Storage Design
* Background Jobs
* Security
* Deployment
* Sequence Diagrams

---

## scripts/

Development utilities.

Examples:

* database initialization
* development setup
* migrations
* maintenance scripts

---

## .github/

GitHub Actions workflows.

Future:

* CI
* Tests
* Docker builds

---

# Backend Structure

```text
backend/

├── app/
├── tests/
├── alembic/
├── pyproject.toml
├── uv.lock
├── Dockerfile
└── .env.example
```

---

# app/

```text
app/

├── api/
├── auth/
├── users/
├── workspaces/
├── documents/
├── chat/
├── search/
├── rag/
├── ai/
├── storage/
├── workers/
├── db/
├── core/
├── common/
└── main.py
```

---

# api/

Contains API routing only.

Example:

```text
api/

v1/

    auth.py

    users.py

    workspaces.py

    documents.py

    chat.py

    search.py
```

Responsibilities:

* route registration
* request handling
* dependency injection

Business logic should never live here.

---

# auth/

Authentication module.

```text
auth/

router.py

service.py

repository.py

schemas.py

jwt.py

password.py

oauth.py
```

Responsibilities:

* login
* registration
* JWT
* OAuth
* password hashing

---

# users/

User management.

```text
users/

router.py

service.py

repository.py

schemas.py
```

---

# workspaces/

Workspace management.

```text
workspaces/

router.py

service.py

repository.py

schemas.py
```

---

# documents/

Document management.

```text
documents/

router.py

service.py

repository.py

schemas.py

validators.py
```

Responsibilities:

* uploads
* metadata
* duplicate detection
* lifecycle management

---

# chat/

Conversation management.

```text
chat/

router.py

service.py

repository.py

schemas.py
```

Responsibilities:

* conversations
* history
* citations

---

# search/

Semantic search endpoints.

```text
search/

router.py

service.py
```

---

# rag/

Retrieval-Augmented Generation.

```text
rag/

retriever.py

chunker.py

reranker.py

pipeline.py
```

Responsibilities:

* retrieval
* chunking
* reranking
* orchestration

---

# ai/

AI-specific services.

```text
ai/

embedding.py

llm.py

prompt_builder.py
```

Responsibilities:

* embedding generation
* LLM abstraction
* prompt construction

---

# storage/

Storage abstraction.

```text
storage/

provider.py

local.py

models.py
```

Future:

* s3.py
* minio.py

---

# workers/

Background processing.

```text
workers/

tasks.py

document_processor.py

queue.py
```

Responsibilities:

* ARQ jobs
* orchestration
* retries

Business logic should remain in services.

---

# db/

Database layer.

```text
db/

models/

session.py

base.py

migrations/
```

Responsibilities:

* SQLAlchemy models
* database session
* metadata

---

# core/

Application-wide infrastructure.

```text
core/

config.py

logging.py

security.py

dependencies.py
```

Responsibilities:

* configuration
* dependency injection
* application settings

---

# common/

Shared reusable utilities.

```text
common/

constants.py

exceptions.py

enums.py

pagination.py

responses.py

utils.py
```

Contains reusable code shared across multiple modules.

---

# Tests

```text
tests/

unit/

integration/

e2e/
```

Testing is separated by scope.

---

# Frontend Structure

```text
frontend/

src/

    api/

    components/

    features/

    hooks/

    layouts/

    pages/

    routes/

    services/

    store/

    styles/

    types/

    utils/

public/

package.json

vite.config.ts
```

---

# Docker Structure

```text
docker/

backend.Dockerfile

frontend.Dockerfile

nginx.conf
```

---

# Documentation Structure

```text
docs/

product-discovery/

architecture/

implementation/

adr-summary.md
```

Architecture documents remain the project's source of truth.

---

# Folder Design Principles

The project follows these principles:

1. Feature-first organization.
2. Business logic separated from API routing.
3. Infrastructure isolated from domain logic.
4. Shared code placed in dedicated modules.
5. AI functionality grouped independently.
6. Future extensibility without major restructuring.

---

# Design Rationale

| Decision                | Rationale                                                                      |
| ----------------------- | ------------------------------------------------------------------------------ |
| Feature-based modules   | Easier navigation and maintenance                                              |
| Repository pattern      | Decouples business logic from persistence                                      |
| Dedicated AI module     | Keeps AI concerns centralized                                                  |
| Separate worker module  | Infrastructure separated from business logic                                   |
| Storage abstraction     | Supports future storage providers                                              |
| Shared `common` package | Prevents code duplication                                                      |
| Root-level separation   | Clear distinction between frontend, backend, infrastructure, and documentation |

---

# Implementation Notes

The folder structure is intended to remain stable throughout the MVP.

New features should integrate into existing modules whenever possible rather than introducing new top-level directories.

If future requirements require significant architectural changes, this document should be updated to remain consistent with the implementation.

---

# Status

**Accepted**

This document should be reviewed whenever:

* major features are added,
* architectural boundaries change,
* deployment strategy changes,
* modules are extracted or merged.
