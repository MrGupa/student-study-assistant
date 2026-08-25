## Architecture Style
Modular Monolith.

## Deployment Style
Docker Compose.

## Frontend
React + TypeScript.

## Backend
FastAPI.

## Primary Database
PostgreSQL.

## Vector Database
Qdrant.

## Background Jobs
Redis + ARQ.

## File Storage
Local filesystem (MVP).
Storage abstraction for future S3/MinIO support.

## OCR Engine
EasyOCR.

## Embeddings
Sentence Transformers.

## LLM Providers
Provider abstraction layer.

## Retrieval Strategy
Simple RAG.

## Authentication
JWT + Google OAuth.

## Integration Test Architecture
The backend uses a dedicated PostgreSQL database for integration testing.

Integration tests use a function-scoped database transaction to isolate
each test from other tests.

The test database flow is:

```text
Test PostgreSQL Database
        ↓
Test Engine
        ↓
Database Connection
        ↓
Explicit Transaction
        ↓
AsyncSession
        ↓
Pytest Fixtures
        ↕
FastAPI Dependency Override
```

## Guiding Principles

1. Keep MVP simple.
2. Avoid overengineering.
3. Prefer modularity.
4. Support future extensibility.
5. Optimize for learning and portfolio value.
6. Abstract infrastructure dependencies.
7. Prefer asynchronous processing.
8. Design for eventual local-first support.
