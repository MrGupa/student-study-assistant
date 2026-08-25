# Git Workflow

## Purpose

This document defines the Git workflow for the Student Study Assistant project.

The objective is to maintain a clean, understandable, and traceable commit history throughout development.

As this project is currently developed by a single developer, the workflow prioritizes simplicity while following industry practices.

---

# Branching Strategy

The project follows a feature branch workflow.

```text
main
│
├── feature/project-setup
├── feature/authentication
├── feature/workspaces
├── feature/documents
├── feature/background-jobs
├── feature/rag
├── feature/chat
├── feature/frontend
└── feature/testing
```

## Main Branch

The `main` branch should always remain in a working state.

Only completed and tested features should be merged into `main`.

Direct commits to `main` should be avoided whenever practical.

---

# Feature Branches

Each major feature or milestone should be implemented in its own branch.

Branch naming convention:

```text
feature/<feature-name>
```

Examples:

```text
feature/project-setup
feature/authentication
feature/workspaces
feature/document-upload
feature/background-processing
feature/rag-chat
feature/search
feature/frontend
```

Bug fixes:

```text
fix/<bug-name>
```

Examples:

```text
fix/upload-validation
fix/token-refresh
```

Refactoring:

```text
refactor/<module-name>
```

Examples:

```text
refactor/document-service
refactor/prompt-builder
```

Documentation:

```text
docs/<topic>
```

Examples:

```text
docs/api
docs/security
```

---

# Commit Message Convention

The project follows the Conventional Commits specification.

Format:

```text
<type>(scope): short description
```

Examples:

```text
feat(auth): implement JWT authentication

feat(documents): add upload endpoint

feat(chat): implement RAG pipeline

fix(storage): handle duplicate uploads

fix(auth): validate refresh token expiry

refactor(search): simplify retrieval pipeline

docs(api): update authentication endpoints

test(chat): add RAG integration tests

chore(deps): update project dependencies
```

---

# Commit Types

| Type     | Purpose                   |
| -------- | ------------------------- |
| feat     | New feature               |
| fix      | Bug fix                   |
| refactor | Internal code improvement |
| docs     | Documentation             |
| test     | Tests                     |
| chore    | Maintenance tasks         |
| ci       | CI/CD changes             |
| perf     | Performance improvements  |

---

# Commit Guidelines

Each commit should:

* represent one logical change,
* compile successfully,
* keep the application in a working state,
* include related tests whenever practical.

Avoid commits that combine unrelated changes.

---

# Development Workflow

For every feature:

```text
Review Architecture
        ↓
Review Sequence Diagram
        ↓
Create Feature Branch
        ↓
Implement
        ↓
Run Tests
        ↓
Refactor
        ↓
Commit
        ↓
Merge into Main
```

---

# Merge Strategy

Use fast-forward or squash merges whenever practical.

The objective is to keep the commit history concise and readable.

---

# Pull Requests

Although this is a single-developer project, every completed feature should be reviewed using a personal checklist before merging.

Checklist:

* Architecture followed
* Tests passing
* Logging reviewed
* Error handling complete
* Documentation updated (if required)
* No unnecessary code
* Formatting completed
* Linting completed

---

# Tags

Project milestones should be tagged.

Examples:

```text
v0.1.0  Project Setup

v0.2.0  Authentication

v0.3.0  Document Upload

v0.4.0  Background Processing

v0.5.0  Semantic Search

v0.6.0  AI Chat

v1.0.0  MVP Release
```

---

# Release Philosophy

Releases should represent stable, working versions of the application.

Every tagged release should:

* build successfully,
* pass tests,
* remain deployable.

---

# Repository Hygiene

The repository should include:

* meaningful commit messages,
* updated README,
* current documentation,
* no generated files,
* no secrets,
* no unnecessary binaries.

Large generated files should not be committed unless required.

---

# Git Ignore

The repository should ignore:

* Python cache files
* Virtual environments
* Node modules
* Environment files
* IDE configuration
* Build artifacts
* Logs
* Temporary files

---

# Development Philosophy

The Git history should tell the story of the project.

A developer reading the commit history should understand:

* what changed,
* why it changed,
* when major features were introduced.

Clean history is more valuable than a large number of commits.

---

# Status

**Accepted**

This workflow applies throughout development unless the project expands to multiple contributors.
