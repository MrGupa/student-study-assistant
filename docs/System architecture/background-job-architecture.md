# Background Job Architecture

## Purpose

This document defines the background job architecture for the Student Study Assistant platform.

Background jobs are responsible for executing long-running and computationally expensive tasks asynchronously without blocking user requests.

The objectives of this architecture are:

* responsive user experience,
* reliable document processing,
* fault tolerance,
* observability,
* scalability,
* future extensibility.

---

# Scope

This document covers:

* Background processing architecture
* Redis queue
* ARQ workers
* Job lifecycle
* Processing pipeline
* Retry strategy
* Failure handling
* Monitoring
* Future scalability

This document does **not** cover:

* Storage implementation
* Authentication
* Deployment configuration
* Database schema

---

# Design Goals

The background processing system should:

1. Keep API requests fast.
2. Execute long-running tasks asynchronously.
3. Recover gracefully from temporary failures.
4. Support future horizontal scaling.
5. Provide visibility into processing progress.
6. Support retries for transient failures.
7. Prevent duplicate processing.

---

# Guiding Principles

## Principle 1 — Asynchronous Processing

Operations expected to take more than a few seconds should execute as background jobs.

Examples:

* OCR
* Chunking
* Embedding generation
* Vector indexing

---

## Principle 2 — One Job per Document (MVP)

Each uploaded document creates exactly one processing job.

The processing job executes multiple sequential stages internally.

Future versions may split these stages into independent jobs without changing the overall pipeline.

---

## Principle 3 — Pipeline-Based Processing

Document processing is treated as a pipeline.

Each stage produces input for the next stage.

This makes the workflow easier to understand, monitor, and extend.

---

## Principle 4 — Idempotent Processing

Background jobs should be safe to retry.

Running the same processing job multiple times should not create duplicate:

* chunks,
* embeddings,
* vector records,
* processing metadata.

---

## Principle 5 — Observable Progress

Users and developers should always know:

* current status,
* current stage,
* failure reason,
* retry attempts.

---

# High-Level Architecture

```text
User Upload
      │
      ▼
FastAPI
      │
      ▼
Create Processing Job
      │
      ▼
Redis Queue
      │
      ▼
ARQ Worker
      │
      ▼
Processing Pipeline
      │
      ▼
PostgreSQL + Qdrant
```

---

# Background Components

## FastAPI

Responsibilities:

* Receive uploads
* Store file metadata
* Create processing job
* Enqueue background task
* Return HTTP 202 Accepted

---

## Redis

Responsibilities:

* Job queue
* Temporary task storage
* Worker communication

Redis is not considered the system of record.

---

## ARQ Worker

Responsibilities:

* Consume queued jobs
* Execute processing pipeline
* Update job status
* Record processing stages
* Handle retries
* Report failures

---

## Document Processing Service

Contains the business logic for:

* text extraction
* OCR
* cleaning
* chunking
* embedding generation
* vector indexing

Workers orchestrate processing but should not contain business logic.

---

# Processing Pipeline

Every uploaded document follows the same logical pipeline.

```text
Upload
    │
    ▼
Text Extraction
    │
    ▼
OCR (if required)
    │
    ▼
Text Cleaning
    │
    ▼
Chunking
    │
    ▼
Embedding Generation
    │
    ▼
Vector Indexing
    │
    ▼
Completed
```

Some stages may be skipped when unnecessary.

Example:

Machine-readable PDF:

```text
Upload
↓
Text Extraction
↓
Cleaning
↓
Chunking
↓
Embedding
↓
Indexing
```

Scanned PDF:

```text
Upload
↓
Text Extraction
↓
OCR
↓
Cleaning
↓
Chunking
↓
Embedding
↓
Indexing
```

---

# Processing Stages

The system uses predefined processing stages.

| Stage           | Description                       |
| --------------- | --------------------------------- |
| uploaded        | File successfully uploaded        |
| text_extraction | Extract embedded text             |
| ocr             | Optical Character Recognition     |
| cleaning        | Normalize extracted text          |
| chunking        | Split into searchable chunks      |
| embedding       | Generate vector embeddings        |
| indexing        | Store vectors in Qdrant           |
| completed       | Processing completed successfully |
| failed          | Processing failed                 |

Using fixed stage names ensures consistency across:

* backend
* frontend
* logs
* monitoring
* documentation

---

# Job Lifecycle

```text
Pending
    │
    ▼
Running
    │
 ┌──┴────────────┐
 │               │
 ▼               ▼
Completed      Failed
                    │
                    ▼
              Retry (if allowed)
```

---

# Job States

Supported job states:

* pending
* running
* completed
* failed
* cancelled

These correspond to the values stored in `document_processing_jobs`.

---

# Stage Tracking

Each processing job records both:

* overall status
* current processing stage

Example:

```text
Status:
Running

Stage:
Embedding
```

If processing fails:

```text
Status:
Failed

Stage:
OCR

Reason:
OCR engine failed.
```

This information should be visible through the API and eventually surfaced in the user interface.

---

# Retry Strategy

Maximum retries:

```text
3
```

Retryable failures use exponential backoff.

Retry schedule:

```text
Attempt 1

↓

Immediate

↓

Attempt 2

↓

Wait 5 seconds

↓

Attempt 3

↓

Wait 15 seconds

↓

Failed
```

---

# Retryable Failures

Examples:

* Redis unavailable
* Temporary filesystem errors
* Network timeout
* Qdrant unavailable
* Temporary embedding model failure

These failures should be retried automatically.

---

# Non-Retryable Failures

Examples:

* Corrupted document
* Unsupported format
* Missing uploaded file
* Validation failure
* Invalid document structure

These failures should immediately mark the job as failed.

Automatic retries should not occur.

---

# Failure Recovery

If a worker crashes during processing:

* incomplete work should not corrupt stored data,
* partially generated artifacts should be cleaned up where possible,
* retry should safely restart processing.

Jobs should always leave the system in a consistent state.

---

# Idempotency Strategy

Background jobs should be safe to execute multiple times.

Before generating new artifacts, processing should verify whether existing artifacts should be replaced.

Examples:

* replace previous chunks,
* replace previous vectors,
* replace processing metadata.

Duplicate retrieval data should never accumulate.

---

# Queue Processing Flow

```text
Upload Document
        │
        ▼
Store File
        │
        ▼
Create Database Record
        │
        ▼
Create Processing Job
        │
        ▼
Enqueue ARQ Job
        │
        ▼
Worker Executes Pipeline
        │
        ▼
Update Stage
        │
        ▼
Completed / Failed
```

---

# Monitoring

The worker should record:

* processing duration
* current stage
* retry count
* failure reason
* queue wait time
* embedding duration
* OCR duration
* indexing duration

These metrics support debugging and future optimization.

---

# User Visibility

Users should be able to observe document progress.

Example:

```text
Operating Systems Notes.pdf

Status:
Running

Current Stage:
Chunking
```

If processing fails:

```text
Operating Systems Notes.pdf

Status:
Failed

Current Stage:
Embedding

Retry Available
```

This improves transparency and simplifies bug reporting.

---

# Cleanup Strategy

When processing fails permanently:

* preserve uploaded file,
* preserve processing history,
* allow manual retry,
* avoid leaving partial vector data.

Temporary processing artifacts should be removed after completion.

---

# Future Enhancements

Future versions may support:

* Multiple workers
* Worker autoscaling
* Stage-specific jobs
* Priority queues
* Scheduled background tasks
* Bulk document processing
* Automatic re-indexing
* Dead-letter queues
* Distributed workers

The current pipeline is intentionally designed so these enhancements require minimal architectural change.

---

# Design Rationale

| Decision                        | Rationale                                                 |
| ------------------------------- | --------------------------------------------------------- |
| Redis + ARQ                     | Lightweight, asynchronous processing suitable for the MVP |
| One processing job per document | Simpler orchestration while preserving future flexibility |
| Pipeline-based processing       | Easier monitoring and future extensibility                |
| Fixed processing stages         | Consistent status reporting throughout the application    |
| Exponential backoff             | Handles transient infrastructure failures gracefully      |
| Three retry limit               | Balances resilience and resource usage                    |
| Stage tracking                  | Improves debugging and user transparency                  |
| Idempotent jobs                 | Safe retries without duplicate data                       |

---

# Implementation Notes

The MVP executes the entire document processing pipeline within a single ARQ job.

If future scalability requires higher throughput, individual pipeline stages may become independent jobs while preserving the same logical workflow.

The background processing architecture should evolve without requiring changes to API endpoints or business services.

---

# Status

**Accepted**

This document should be reviewed whenever:

* processing stages change,
* background infrastructure changes,
* retry policies change,
* worker scaling requirements change,
* document ingestion requirements evolve.
