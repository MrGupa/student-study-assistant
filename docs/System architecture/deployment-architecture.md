# Deployment Architecture

## Purpose

This document defines the deployment architecture for the Student Study Assistant platform.

The deployment architecture describes how application components are packaged, deployed, configured, and connected in both development and production environments.

The objectives are:

* reproducible deployments,
* modular infrastructure,
* maintainability,
* operational simplicity,
* future scalability.

---

# Scope

This document covers:

* Development deployment
* Production deployment
* Container architecture
* Service communication
* Persistent storage
* Networking
* Environment configuration
* Health checks
* Startup strategy

This document does **not** cover:

* CI/CD pipelines
* Cloud provider configuration
* Kubernetes
* Infrastructure as Code

---

# Deployment Goals

The deployment architecture should:

1. Keep local development simple.
2. Match production architecture as closely as practical.
3. Isolate infrastructure services.
4. Support persistent data.
5. Allow independent service restarts.
6. Support future horizontal scaling.
7. Minimize deployment complexity for the MVP.

---

# Guiding Principles

## Principle 1 — One Service, One Responsibility

Each service performs a single responsibility.

Services should be independently deployable and restartable.

---

## Principle 2 — Infrastructure Isolation

Infrastructure services remain independent from application services.

Examples:

* PostgreSQL
* Redis
* Qdrant

should not be bundled into the backend container.

---

## Principle 3 — Environment-Based Configuration

Configuration should be provided through environment variables.

Application code should never contain environment-specific values.

---

## Principle 4 — Persistent User Data

Containers are disposable.

User data is not.

Persistent data must always be stored using Docker volumes.

---

## Principle 5 — Development Optimized for Productivity

Developer experience takes priority during development.

The frontend runs locally using Vite for faster feedback.

Infrastructure services run inside Docker.

---

# High-Level Deployment Architecture

## Development

```text
Developer

│

├── React (npm run dev)

│

└── Docker Compose

      ├── FastAPI
      ├── PostgreSQL
      ├── Redis
      ├── Qdrant
      └── ARQ Worker
```

---

## Production

```text
Internet

↓

Nginx

├── React Static Files

↓

FastAPI

├── PostgreSQL
├── Redis
├── Qdrant
└── ARQ Worker
```

---

# Deployment Components

## React Frontend

Development:

Runs locally using:

```text
npm run dev
```

Advantages:

* Fast hot reload
* Better debugging
* Faster startup
* Improved developer productivity

Production:

Served as static files from an Nginx container.

---

## FastAPI Backend

Responsibilities:

* REST API
* Authentication
* Authorization
* Search
* Chat orchestration
* Background job creation

Runs inside a dedicated container.

---

## PostgreSQL

Stores:

* users
* workspaces
* documents
* chats
* metadata

Uses a persistent Docker volume.

---

## Redis

Responsibilities:

* ARQ job queue
* Worker communication

Redis is treated as temporary infrastructure rather than persistent storage.

---

## Qdrant

Stores vector embeddings.

Uses a dedicated persistent volume.

---

## ARQ Worker

Runs independently from the backend.

Responsibilities:

* OCR
* Chunking
* Embedding generation
* Indexing

Worker failures should never stop API requests.

---

# Container Architecture

Each major service runs inside its own container.

```text
Frontend (Development)

↓

Backend Container

↓

PostgreSQL Container

↓

Redis Container

↓

Qdrant Container

↓

Worker Container
```

Benefits:

* Isolation
* Independent restarts
* Easier debugging
* Better scalability

---

# Service Communication

Docker networking enables communication using service names.

Example:

```text
Backend

↓

postgres

↓

redis

↓

qdrant
```

Service names should be used instead of fixed IP addresses.

Example:

```text
DATABASE_HOST=postgres

REDIS_HOST=redis

QDRANT_HOST=qdrant
```

---

# Persistent Storage

Persistent Docker volumes are required for:

| Service            | Persistent Volume |
| ------------------ | ----------------- |
| PostgreSQL         | Yes               |
| Qdrant             | Yes               |
| Uploaded Documents | Yes               |
| Redis              | No                |

Volumes ensure user data survives container recreation.

---

# Environment Configuration

Application configuration is provided through environment variables.

Backend examples:

```text
DATABASE_URL

REDIS_URL

QDRANT_URL

JWT_SECRET

GOOGLE_CLIENT_ID

GOOGLE_CLIENT_SECRET
```

Frontend examples:

```text
VITE_API_BASE_URL
```

Worker examples:

```text
DATABASE_URL

REDIS_URL

QDRANT_URL
```

Secrets must never be committed to version control.

---

# Startup Order

Infrastructure services should start before application services.

Conceptually:

```text
PostgreSQL

↓

Redis

↓

Qdrant

↓

FastAPI

↓

ARQ Worker
```

The application should tolerate temporary infrastructure unavailability by retrying connections during startup.

---

# Health Checks

Each service should expose health information.

Backend:

```text
/api/v1/health/live

/api/v1/health/ready
```

Docker health checks should be configured for:

* PostgreSQL
* Redis
* Qdrant

Application startup should depend on healthy infrastructure whenever possible.

---

# Reverse Proxy

Production deployments include an Nginx reverse proxy.

Responsibilities:

* Serve React static files
* Forward API requests to FastAPI
* HTTPS termination
* Response compression
* Static asset caching

Development deployments do not require a reverse proxy.

---

# Networking

Docker Compose creates an isolated bridge network for all containers.

External access:

* React (development)
* Nginx (production)

Internal services communicate only through the Docker network.

The database, Redis, and Qdrant should not be exposed directly to the public internet.

---

# Data Persistence

The following data survives container recreation:

* PostgreSQL database
* Uploaded documents
* Qdrant vector data

Temporary data:

* Redis queues
* Temporary processing files

These may be safely recreated.

---

# Failure Recovery

If an application container stops unexpectedly:

* Docker restarts the container.
* Persistent data remains intact.
* Background processing resumes when the worker is available.

Infrastructure failures should not corrupt stored user data.

---

# Scalability

The MVP deploys:

* one backend instance,
* one worker,
* one PostgreSQL instance,
* one Redis instance,
* one Qdrant instance.

Future versions may support:

* multiple backend replicas,
* multiple workers,
* load balancing,
* managed databases,
* managed object storage.

The deployment architecture should support these enhancements without requiring application redesign.

---

# Deployment Environments

## Local Development

Purpose:

Feature development and debugging.

Characteristics:

* React runs locally.
* Infrastructure uses Docker Compose.
* Hot reload enabled.

---

## Production

Purpose:

End-user deployment.

Characteristics:

* Containerized frontend
* Nginx reverse proxy
* Docker Compose
* HTTPS
* Persistent volumes
* Environment-specific configuration

---

# Future Enhancements

Potential future improvements include:

* GitHub Actions CI/CD
* Automated Docker image publishing
* Cloud deployment
* Managed PostgreSQL
* Managed Redis
* Managed Qdrant
* Object storage (S3/MinIO)
* Kubernetes
* Horizontal autoscaling
* Centralized logging

---

# Design Rationale

| Decision                                | Rationale                                  |
| --------------------------------------- | ------------------------------------------ |
| Docker Compose                          | Simple, widely used, ideal for an MVP      |
| Separate containers                     | Better isolation and maintainability       |
| React outside Docker during development | Faster development workflow                |
| Containerized frontend in production    | Consistent deployment                      |
| Persistent Docker volumes               | Protect user data                          |
| Nginx reverse proxy                     | Production-ready request handling          |
| Environment variables                   | Secure, environment-specific configuration |
| Service-name networking                 | Portable and maintainable deployments      |

---

# Implementation Notes

Development prioritizes developer productivity while maintaining architectural consistency with production.

The production deployment intentionally remains simple and avoids orchestration platforms such as Kubernetes.

This deployment model is appropriate for the expected scale of the MVP while leaving clear migration paths for future growth.

---

# Status

**Accepted**

This document should be reviewed whenever:

* deployment strategy changes,
* cloud providers are introduced,
* scaling requirements change,
* infrastructure services are replaced,
* CI/CD pipelines are added.
