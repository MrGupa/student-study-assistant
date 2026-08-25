# Coding Standards

## Purpose

This document defines the coding standards for the Student Study Assistant project.

The objective is to maintain a clean, consistent, maintainable, and production-quality codebase throughout development.

These standards apply to both backend and frontend development unless stated otherwise.

---

# Guiding Principles

The project follows these principles:

1. Readability over cleverness.
2. Simplicity over unnecessary abstraction.
3. Explicit is better than implicit.
4. Consistency over personal preference.
5. Small, focused modules.
6. Strong typing whenever practical.

---

# General Conventions

## Naming

Use descriptive names.

Good:

```python
document_service
workspace_repository
generate_embeddings()
```

Avoid:

```python
ds
repo
process()
temp()
```

Code should be understandable without additional explanation.

---

## File Names

Use:

```text
snake_case.py
```

Examples:

```text
document_service.py
storage_provider.py
prompt_builder.py
```

---

## Folder Names

Use:

```text
lowercase
```

Examples:

```text
documents
chat
storage
workers
```

---

# Python Standards

## Python Version

Use the latest stable Python version supported by project dependencies.

---

## Type Hints

Every public function should include type hints.

Example:

```python
def create_workspace(
    user_id: UUID,
    request: WorkspaceCreateRequest,
) -> Workspace:
```

Avoid untyped public APIs.

---

## Function Size

Functions should perform one responsibility.

Recommended:

* 10–30 lines

Investigate refactoring when functions consistently exceed:

* 50 lines

---

## Class Size

Classes should represent a single responsibility.

Avoid "God classes" responsible for multiple domains.

---

## Docstrings

Use docstrings only for public classes, public functions, and modules where additional context is valuable.

Avoid redundant docstrings.

Bad:

```python
"""Returns the user."""
```

Good:

```python
"""Creates a workspace after validating ownership and uniqueness."""
```

---

# Architecture Rules

## Router

Routers should:

* validate requests,
* call services,
* return responses.

Routers must not contain business logic.

---

## Service

Services contain business logic.

Services should not perform direct SQL queries.

---

## Repository

Repositories manage persistence.

Repositories should not contain business rules.

---

## Dependency Direction

The dependency flow should remain:

```text
Router
    ↓
Service
    ↓
Repository
    ↓
Database
```

Reverse dependencies are not permitted.

---

# Database Standards

Use SQLAlchemy ORM whenever possible.

Avoid string-based SQL construction.

Use UUIDs as primary keys.

Database transactions should remain short.

---

# API Standards

REST endpoints should:

* use nouns,
* follow REST conventions,
* return consistent response structures.

Examples:

```text
POST /workspaces

GET /documents

DELETE /documents/{id}
```

Avoid verb-based endpoints.

---

# Error Handling

Raise domain-specific exceptions.

Avoid generic:

```python
Exception
```

Create meaningful exception classes.

Return user-friendly API responses.

Internal errors should be logged.

---

# Logging

Use structured logging.

Log:

* application startup,
* authentication events,
* background jobs,
* processing failures,
* unexpected exceptions.

Never log:

* passwords,
* JWTs,
* refresh tokens,
* API keys,
* authorization headers.

---

# Configuration

Configuration values belong in environment variables.

Never hardcode:

* secrets,
* URLs,
* credentials,
* ports.

Application code should access configuration through the centralized configuration module.

---

# Background Jobs

Workers should orchestrate work.

Business logic belongs inside services.

Workers should:

* update processing status,
* handle retries,
* report failures.

---

# Storage

Application code should interact only with the Storage Provider abstraction.

Never access the filesystem directly outside the storage module.

---

# AI Standards

Prompt construction belongs in the AI module.

LLM providers must remain replaceable.

Embedding generation should be abstracted behind interfaces.

Avoid embedding provider-specific logic throughout the application.

---

# Frontend Standards

Use:

* TypeScript
* Functional components
* Hooks
* Feature-based organization

Avoid class components.

Prefer composition over inheritance.

---

# React Guidelines

Keep components focused.

Move business logic into hooks or services.

Prefer reusable components over duplication.

---

# State Management

Use:

* TanStack Query for server state.
* Zustand for client state.

Avoid storing server data in Zustand.

---

# Formatting

Backend:

* Ruff
* Black-compatible formatting

Frontend:

* ESLint
* Prettier

Formatting should be automatic.

Do not manually format code.

---

# Imports

Import order:

1. Standard library
2. Third-party packages
3. Local application modules

Avoid wildcard imports.

---

# Comments

Comments should explain:

* why something exists,
* non-obvious decisions,
* architectural reasoning.

Avoid comments that describe obvious code.

Bad:

```python
# Increment counter
counter += 1
```

---

# Testing Standards

Every new feature should include appropriate tests.

Testing order:

1. Unit tests
2. Integration tests
3. End-to-end tests (where applicable)

Bug fixes should include regression tests whenever practical.

---

# Git Standards

Each commit should represent a single logical change.

Avoid mixing unrelated modifications.

Commit frequently.

---

# Code Review Checklist

Before merging code, verify:

* Code follows architecture.
* No duplicated logic.
* Type hints are present.
* Tests pass.
* Logging is appropriate.
* Error handling is complete.
* Documentation is updated if required.

---

# Refactoring Guidelines

Refactor when:

* duplication appears,
* functions become difficult to read,
* responsibilities become unclear,
* module boundaries are violated.

Do not refactor without a measurable improvement.

---

# Technical Debt

When shortcuts are necessary:

* document them,
* isolate them,
* schedule future improvements.

Do not leave undocumented technical debt.

---

# Design Philosophy

The project emphasizes:

* maintainability,
* modularity,
* readability,
* explicit architecture,
* production-oriented engineering.

The objective is not merely to produce a working application, but to produce code that remains understandable and maintainable as the project grows.

---

# Status

**Accepted**

This document applies to all future development unless superseded by a later architectural decision.
