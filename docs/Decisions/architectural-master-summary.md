# Consolidated Architecture & Product Decision Summary

**Project:** Student Study Assistant
**Status:** Consolidated reference
**Source:** Previous architectural decision summary + ADR-001 through ADR-013
**Last reviewed:** 25 August 2026

---

## 1. Product Vision

The product is an **AI-powered learning workspace and personalized study assistant**, rather than a generic PDF/RAG chatbot.

The product exists to help students learn more effectively from their existing study material, particularly under examination time constraints.

The central product principle is:

> **Help students learn the right things at the right depth within their limited time.**

The product optimizes for **learning efficiency rather than maximum content consumption**.

---

## 2. Target User and MVP Model

The MVP is primarily designed for **university students managing their own study material**.

Future expansion may include competitive-exam aspirants, researchers, teachers, and working professionals.

The underlying system nevertheless uses a **single generic User model**. Personas are product-design concepts rather than separate authorization roles or dashboards, allowing one user to potentially fit multiple personas.

The MVP is **single-user**:

* No collaboration
* No organizations
* No shared workspaces

Collaboration is a later capability. This keeps the initial product focused and simplifies authorization.

---

## 3. Product Priorities

The product prioritizes, in order:

1. **Learning efficiency**
2. Information organization
3. Syllabus awareness
4. Topic prioritization

It should not initially become a generic tutoring platform. Features that increase information overload or do not improve learning efficiency are deliberately deprioritized.

Product success is primarily defined as:

> **Improving learning efficiency.**

The intended outcome is helping students learn the right material at the appropriate depth in the least amount of time. Measuring this may eventually require user feedback, surveys, and educational-outcome metrics.

---

## 4. Product Differentiation

The platform competes on **educational context rather than generic AI capability**.

Its differentiation comes from:

* Syllabus-aware learning
* Assessment-aware explanations
* Personalized learning context
* Workspace-based organization
* Affordable AI options

Document chat alone is not considered sufficient differentiation.

---

## 5. Workspace and Knowledge Organization

Knowledge is organized into **Workspaces**.

For the MVP:

> **Workspace = Subject**

Examples include Operating Systems, Database Management Systems, and Computer Networks.

A workspace contains the student's:

* Documents
* Chats
* Summaries
* Generated study aids

The broader architectural concept remains extensible to other workspace/group concepts in the future.

### Retrieval scope

**MVP:** Search only within the active workspace.

**Future:** User-selected multi-workspace search, Workspace Groups, and potentially global search.

This improves retrieval relevance and simplifies authorization while leaving room for future cross-workspace functionality.

---

## 6. Personalized Learning Memory

The system maintains **user learning memory**.

### MVP

* Chat history
* User preferences
* Workspace preferences
* Answer-formatting preferences

### Later

* Quiz performance
* Weak topics
* Learning analytics
* Learning goals
* Adaptive recommendations
* Personalized tutoring information

Memory is a major personalization and differentiation mechanism, but introduces additional database complexity, privacy considerations, and implementation effort.

**Roadmap clarification:** Weak-topic detection is explicitly a **Phase 2** feature in the MVP roadmap, despite the earlier memory ADR describing weak topics under MVP+.

---

## 7. Syllabus-Aware Learning

The platform supports **Syllabus-Aware Learning**.

Users may optionally provide:

* Syllabus documents
* Previous-year papers
* Assessment materials

These resources are used to tailor explanations to the student's educational context.

By default, AI responses should remain within syllabus boundaries. Users can explicitly request deeper explanations.

Syllabus upload is optional to avoid onboarding friction.

This capability directly supports the Learning Efficiency First principle and the product's differentiation strategy.

---

## 8. MVP and Product Roadmap

### Core MVP

* Authentication
* User profiles
* Workspace management
* Document upload
* Document processing pipeline
* Semantic search
* Chat with documents
* Chat history
* Basic user preferences

### MVP+

* Flashcards
* Quizzes
* Learning analytics

### Phase 2

* Audio understanding
* Image understanding
* Study plans
* Weak-topic detection
* Multi-workspace search
* Citations

### Phase 3

* Personalized tutor
* Collaboration
* Exam simulations
* Adaptive learning

The MVP's purpose is to validate whether students obtain meaningful value from AI-powered interaction with their study materials before investing in advanced learning capabilities.

---

# 9. Application Architecture

The backend uses a **modular monolith**.

The application is divided into clear feature modules while remaining a single deployable application. This keeps development simple without abandoning future architectural flexibility.

### Code organization

Backend code follows a **feature-based structure**, rather than being organized primarily by technical layers.

### Business logic

Business services access persistence through the **Repository Pattern**.

### Dependency management

Shared services are supplied through **FastAPI dependency injection**, improving modularity and testability.

---

# 10. Backend Technology

The selected backend stack is:

* **FastAPI** — application/API framework
* **PostgreSQL** — primary relational database
* **Qdrant** — vector database for embeddings and semantic retrieval
* **Redis + ARQ** — asynchronous background processing

FastAPI was selected for async support, typing, and automatic OpenAPI generation. PostgreSQL provides reliable relational storage and JSONB support. Qdrant handles semantic search and metadata filtering. Redis/ARQ provides lightweight background-job processing appropriate to the project's scale.

---

# 11. Authentication and Authorization

Authentication uses:

> **JWT access tokens + refresh tokens**

Google OAuth is supported alongside traditional email/password authentication to reduce onboarding friction.

Authorization is **ownership-based**.

Every workspace, document, and conversation belongs to a single user, and access is controlled accordingly.

This aligns with the single-user MVP and the workspace-based organization model.

---

# 12. Document Security

Uploaded documents are treated as **untrusted input**.

Document contents must not be allowed to override system instructions or otherwise manipulate the application's behavior.

This decision exists primarily to mitigate prompt injection and preserve system-level instructions.

---

# 13. File Storage

File storage is abstracted behind a **Storage Provider interface**.

For the MVP, the implementation uses the **local filesystem**.

The abstraction permits future migration to S3, MinIO, or another object-storage system without changing business logic.

Uploaded files use **UUID-based filenames** to avoid collisions and simplify storage management.

Duplicate uploads are detected using **SHA-256 hashes**, making duplicate detection independent of the original filename.

---

# 14. Document Processing

Each uploaded document creates **one ARQ processing job**.

Document processing follows a **stage-based pipeline**, making processing state observable and allowing user feedback around individual stages.

Transient processing failures are retried **up to three times using exponential backoff**.

---

# 15. RAG Architecture

AI responses use **Retrieval-Augmented Generation**.

Relevant document context is retrieved and supplied to the model so responses are grounded in the user's study material.

AI and embedding providers are abstracted behind interfaces to avoid vendor lock-in.

### Retrieval boundary

The active workspace is the default retrieval boundary.

This improves relevance and aligns retrieval with ownership/authorization boundaries.

### Conversation context

Conversation context uses a combination of:

* Recent messages
* Conversation summaries

This balances contextual continuity against token usage.

---

# 16. Deployment

The deployment strategy uses **Docker Compose** for reproducible local and production environments.

The background worker runs in a **separate container** from the API so long-running processing does not block API responsiveness.

During development, the **React frontend runs outside Docker** for developer productivity. It is containerized for production deployment.

---

# 17. Development Process

Development follows two explicit principles.

### Architecture First

Architecture is completed before implementation to reduce architectural uncertainty.

### Milestone Based

Implementation proceeds incrementally through milestones, with each milestone producing a working and testable increment.

This reduces integration risk and prevents the project from becoming a large untested implementation.

---

# 18. Integration Testing

Integration tests use a **dedicated PostgreSQL test database**, never the development database.

Each database integration test:

1. Obtains a connection from the test engine.
2. Begins an explicit transaction.
3. Creates an `AsyncSession` bound to that connection.
4. Shares that session between pytest fixtures and the FastAPI database dependency through dependency overriding.
5. Uses `flush()` when generated values or in-transaction visibility are required.
6. Avoids committing test data.
7. Rolls the transaction back after the test.

The database-session fixture owns the transaction lifecycle.

This provides real PostgreSQL integration while ensuring test data cannot persist between tests or contaminate development data.

Manual cleanup and independent fixture/API sessions are rejected in favor of transaction rollback.

---

# 19. Architectural Principles Derived from the Decisions

Taken together, the decisions establish these overarching principles:

### Product

**Learning efficiency over content volume.**

### User

**University students first, but maintain a generic user model.**

### Organization

**Subject-based workspaces are the primary MVP boundary.**

### Retrieval

**Keep retrieval contextual, relevant, and workspace-scoped.**

### Personalization

**Maintain progressively richer learning memory.**

### AI

**Ground responses in user material and abstract AI providers.**

### Security

**Treat user-uploaded content as untrusted.**

### Architecture

**Prefer a modular monolith with clear boundaries over premature distributed architecture.**

### Infrastructure

**Use simple, replaceable infrastructure with abstraction at important external boundaries.**

### Development

**Architecture first, then incremental milestone-based implementation.**

### Testing

**Use the real PostgreSQL stack while isolating every integration test transaction.**

---

# 20. Decision Hierarchy for Future Features

When evaluating a new feature, the decisions collectively imply this order of questions:

1. **Does it improve learning efficiency?**
2. **Does it help students learn the right material at the right depth?**
3. **Does it respect educational/syllabus context?**
4. **Does it fit the subject/workspace model?**
5. **Does it support personalization without unnecessary complexity?**
6. **Does it fit the current MVP phase?**
7. **Does it preserve the modular architecture and existing ownership boundaries?**
8. **Does it introduce infrastructure complexity that is justified by the product value?**

Features that fail the learning-efficiency test or primarily increase information volume should generally be deprioritized.

---

# 21. Reconciled Decisions / Source-of-Truth Rules

The following interpretations should be used when the individual documents appear to overlap:

* **Workspace:** MVP workspace is a **Subject**; the underlying architecture remains extensible for future workspace/group concepts.
* **Weak-topic detection:** **Phase 2**, despite the earlier memory ADR's MVP+ classification.
* **Single-user MVP:** collaboration and shared workspaces remain future capabilities.
* **Generic User model:** does not contradict the student-first product; it is an architectural choice that keeps future expansion possible.
* **Syllabus-aware learning:** an accepted product capability and major differentiator; its exact placement in the MVP feature list should be explicitly clarified before implementation if phase precision is required.
* **Citations:** RAG is part of the architecture, but the product roadmap explicitly places the user-facing Citations feature in Phase 2.
* **Integration testing:** dedicated PostgreSQL + transaction rollback is the current testing standard and is independent of the product roadmap.

---

# 22. Authoritative Status

This consolidated document is a **reference summary**, not a replacement for the individual ADRs.

The individual ADRs contain the detailed context, alternatives, rationale, and consequences.

If a future implementation decision changes one of these architectural choices, the relevant ADR should be updated and this summary should subsequently be reconciled with it.
