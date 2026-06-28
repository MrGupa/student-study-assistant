# Student Study Assistant

> An AI-powered study assistant designed to help university students organize study materials, generate learning resources, and interact with their knowledge through Retrieval-Augmented Generation (RAG).

---

## Project Status

**Status:** 🚧 Under Active Development

This project is currently in the implementation phase. The architecture and system design have been completed, and development is progressing incrementally following a milestone-based roadmap.

---

## Why This Project?

The Student Study Assistant is being developed as a production-oriented full-stack AI application that demonstrates modern software engineering practices alongside applied machine learning.

The primary objectives of this project are to:

* Build a scalable AI-powered study platform for university students.
* Demonstrate clean architecture and modular system design.
* Apply Retrieval-Augmented Generation (RAG) for educational use cases.
* Follow professional software engineering practices throughout the entire development lifecycle.
* Serve as a portfolio project showcasing backend engineering, frontend development, DevOps fundamentals, and AI integration.

Rather than focusing solely on delivering features, this project emphasizes maintainability, scalability, testing, documentation, and iterative development.

---

## Planned Features

The MVP is expected to include:

* Secure user authentication and authorization
* Study material management
* AI-powered question answering using Retrieval-Augmented Generation (RAG)
* Automatic note generation
* Flashcard generation
* Semantic document search
* Study session management
* Background processing for long-running AI tasks
* Responsive web interface

Additional features may be introduced in future iterations based on project goals and user feedback.

---

## Architecture Overview

The application follows a modular monorepo architecture with clear separation of concerns between frontend, backend, infrastructure, and supporting resources.

```text
student-study-assistant/
│
├── backend/          # FastAPI backend
├── frontend/         # React frontend
├── infra/            # Infrastructure configuration
├── docs/             # Project documentation
├── scripts/          # Development and maintenance scripts
└── .github/          # CI/CD workflows
```

The architecture has been designed to support future scalability, maintainability, and production deployment.

---

## Technology Stack

| Layer                      | Technology          |
| -------------------------- | ------------------- |
| Backend                    | FastAPI             |
| Frontend                   | React + TypeScript  |
| Database                   | PostgreSQL          |
| Vector Database            | Qdrant              |
| Cache                      | Redis               |
| Background Jobs            | ARQ                 |
| ORM                        | SQLAlchemy          |
| Database Migrations        | Alembic             |
| Python Package Manager     | uv                  |
| JavaScript Package Manager | pnpm                |
| Containerization           | Docker              |
| Development Environment    | WSL2 (Ubuntu 24.04) |

---

## Development Philosophy

This project is being developed using an engineering-first workflow:

1. Requirements Analysis
2. Architecture Design
3. Database Design
4. API Design
5. Incremental Implementation
6. Testing
7. Refactoring
8. Documentation
9. Deployment
10. Continuous Improvement

Each milestone is treated as a small engineering project rather than simply implementing features.

---

## Roadmap

The current implementation roadmap includes:

* Development environment setup
* Repository initialization
* Backend foundation
* Frontend foundation
* Authentication and authorization
* Study material management
* AI and RAG pipeline
* Flashcard and note generation
* Background processing
* Testing
* Production deployment

---

## Documentation

Comprehensive documentation will accompany the implementation, including:

* System Architecture
* Architectural Decision Records (ADRs)
* API Documentation
* Database Design
* Deployment Guide
* Development Guide

Documentation will be expanded as implementation progresses.

---

## License

This project will be released under the MIT License.

---

## Author

**Gaurav**

Final-year Computer Engineering Student

Mumbai University
