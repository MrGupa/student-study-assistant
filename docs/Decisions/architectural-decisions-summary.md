# Architecture Decision Summary (ADR)

## Purpose

This document consolidates the major architectural decisions made during the design phase of the Student Study Assistant project.

Unlike traditional Architecture Decision Records (ADRs), which are maintained as separate chronological documents, this project groups decisions by architectural area.

The objective is to provide a single reference during implementation that captures **what was decided**, **why it was decided**, and **whether the decision is still current**.

---

# ADR Format

Each ADR follows the same structure.

**Decision**

The architectural decision that was accepted.

**Rationale**

Why the decision was made.

**Status**

Accepted unless otherwise noted.

---

# Product Decisions

## ADR-001 — Student-First Product

**Decision**

The platform is designed primarily for university students managing their own study material.

**Rationale**

A clearly defined target audience keeps the MVP focused and avoids unnecessary features.

**Status**

Accepted

---

## ADR-002 — Workspace-Centric Organization

**Decision**

Documents, chats, and search operate within a workspace.

**Rationale**

Provides natural organization, authorization boundaries, and retrieval scope.

**Status**

Accepted

---

## ADR-003 — Single-User MVP

**Decision**

The MVP supports individual users only.

**Rationale**

Reduces complexity by excluding collaboration, organizations, and shared workspaces.

**Status**

Accepted

---

# Application Architecture

## ADR-004 — Modular Monolith

**Decision**

Implement the application as a modular monolith.

**Rationale**

Simplifies development while maintaining clear module boundaries for future evolution.

**Status**

Accepted

---

## ADR-005 — Feature-Based Project Structure

**Decision**

Organize backend code by feature rather than by technical layer.

**Rationale**

Improves navigation, maintainability, and future scalability.

**Status**

Accepted

---

## ADR-006 — Repository Pattern

**Decision**

Business services access persistence through repositories.

**Rationale**

Separates business logic from database implementation.

**Status**

Accepted

---

## ADR-007 — Dependency Injection

**Decision**

Shared services are provided through FastAPI dependency injection.

**Rationale**

Improves modularity and testability.

**Status**

Accepted

---

# Backend Technology

## ADR-008 — FastAPI

**Decision**

Use FastAPI as the backend framework.

**Rationale**

Excellent async support, automatic OpenAPI generation, and strong typing.

**Status**

Accepted

---

## ADR-009 — PostgreSQL

**Decision**

Use PostgreSQL as the primary relational database.

**Rationale**

Reliable relational storage with JSONB support and mature tooling.

**Status**

Accepted

---

## ADR-010 — Qdrant

**Decision**

Store vector embeddings in Qdrant.

**Rationale**

Supports efficient semantic search and metadata filtering.

**Status**

Accepted

---

## ADR-011 — Redis + ARQ

**Decision**

Use Redis and ARQ for asynchronous background processing.

**Rationale**

Lightweight solution that fits the project's scale.

**Status**

Accepted

---

# Authentication & Security

## ADR-012 — JWT Authentication

**Decision**

Use JWT access tokens with refresh tokens.

**Rationale**

Provides stateless authentication while maintaining good user experience.

**Status**

Accepted

---

## ADR-013 — Google OAuth

**Decision**

Support Google OAuth in addition to email/password authentication.

**Rationale**

Reduces onboarding friction while preserving traditional authentication.

**Status**

Accepted

---

## ADR-014 — Ownership-Based Authorization

**Decision**

Authorize access based on resource ownership.

**Rationale**

Every workspace, document, and conversation belongs to a single user.

**Status**

Accepted

---

## ADR-015 — Treat Uploaded Documents as Untrusted

**Decision**

Uploaded documents are treated as untrusted input.

**Rationale**

Mitigates prompt injection and protects system instructions.

**Status**

Accepted

---

# Storage

## ADR-016 — Storage Provider Abstraction

**Decision**

Use a Storage Provider interface with a local filesystem implementation for the MVP.

**Rationale**

Supports future migration to S3 or MinIO without changing business logic.

**Status**

Accepted

---

## ADR-017 — UUID Filenames

**Decision**

Store uploaded files using UUID-based filenames.

**Rationale**

Avoids filename collisions and simplifies storage management.

**Status**

Accepted

---

## ADR-018 — SHA-256 Duplicate Detection

**Decision**

Detect duplicate uploads using SHA-256 hashes.

**Rationale**

Reliable duplicate detection independent of filenames.

**Status**

Accepted

---

# Background Processing

## ADR-019 — One Processing Job per Document

**Decision**

Each uploaded document creates one ARQ processing job.

**Rationale**

Simplifies orchestration while preserving future scalability.

**Status**

Accepted

---

## ADR-020 — Stage-Based Processing Pipeline

**Decision**

Document processing follows predefined stages.

**Rationale**

Improves observability and user feedback.

**Status**

Accepted

---

## ADR-021 — Exponential Backoff Retries

**Decision**

Retry transient failures up to three times using exponential backoff.

**Rationale**

Improves resilience without excessive complexity.

**Status**

Accepted

---

# RAG Architecture

## ADR-022 — Retrieval-Augmented Generation

**Decision**

Ground AI responses using retrieved document context.

**Rationale**

Improves factual accuracy and provides citations.

**Status**

Accepted

---

## ADR-023 — Single Workspace Retrieval

**Decision**

Search only within the active workspace.

**Rationale**

Improves relevance and simplifies authorization.

**Status**

Accepted

---

## ADR-024 — Provider Abstraction for AI

**Decision**

Abstract LLM and embedding providers behind interfaces.

**Rationale**

Avoids vendor lock-in.

**Status**

Accepted

---

## ADR-025 — Conversation Memory Strategy

**Decision**

Use conversation summaries together with recent messages.

**Rationale**

Balances context quality with token usage.

**Status**

Accepted

---

# Deployment

## ADR-026 — Docker Compose

**Decision**

Use Docker Compose for local and production deployments.

**Rationale**

Simple, reproducible deployment suitable for the MVP.

**Status**

Accepted

---

## ADR-027 — Separate Worker Container

**Decision**

Deploy the background worker independently from the API.

**Rationale**

Long-running jobs should not block API responsiveness.

**Status**

Accepted

---

## ADR-028 — React Outside Docker During Development

**Decision**

Run the React frontend locally during development and containerize it only for production.

**Rationale**

Improves developer productivity while maintaining production consistency.

**Status**

Accepted

---

# Development Practices

## ADR-029 — Architecture-First Development

**Decision**

Complete architecture before implementation.

**Rationale**

Reduces architectural uncertainty during development.

**Status**

Accepted

---

## ADR-030 — Milestone-Based Implementation

**Decision**

Implement the project incrementally using milestone-driven development.

**Rationale**

Each milestone delivers a working, testable increment while reducing integration risk.

**Status**

Accepted

---

# Document Status

This document serves as the authoritative summary of architectural decisions for the project.

If implementation requires changing an architectural decision, the relevant ADR should be updated to reflect the new direction.
