# Storage Design

## Purpose

This document defines the storage architecture for the Student Study Assistant platform.

The storage layer is responsible for managing uploaded documents throughout their lifecycle while remaining independent of the underlying storage technology.

The objectives of this design are:

* simplicity,
* maintainability,
* storage provider abstraction,
* future extensibility,
* secure file management,
* compatibility with future cloud storage providers.

This document complements the Database Design by defining how physical files are stored rather than how metadata is persisted.

---

# Scope

This document covers:

* Physical file storage
* Storage provider abstraction
* Directory organization
* File naming strategy
* Upload lifecycle
* File deletion
* Duplicate detection
* Temporary storage
* Backup strategy
* Future storage providers

This document does **not** cover:

* Database schema
* Vector database internals
* Background processing implementation
* Deployment configuration

---

# Design Goals

The storage architecture should:

1. Store uploaded files safely.
2. Hide storage implementation behind an abstraction.
3. Support future storage providers without changing business logic.
4. Prevent filename collisions.
5. Keep storage organized and easy to debug.
6. Minimize unnecessary duplication.
7. Support efficient backup and recovery.

---

# Guiding Principles

## Principle 1 — Separate Storage Logic from Business Logic

Business services should never interact directly with the filesystem.

Instead, all storage operations should pass through a Storage Provider interface.

---

## Principle 2 — Storage Providers are Replaceable

The application should support multiple storage providers.

The MVP uses:

* Local filesystem

Future versions may support:

* Amazon S3
* MinIO
* Azure Blob Storage
* Google Cloud Storage

Replacing the storage provider should not require changes to application services.

---

## Principle 3 — Files are Immutable

Uploaded documents are treated as immutable.

Renaming a document changes only its metadata.

The physical file is never renamed after upload.

---

## Principle 4 — Metadata is Stored Separately

Physical files and metadata are separate concerns.

File metadata belongs in PostgreSQL.

Binary content belongs in the storage provider.

---

## Principle 5 — Derived Data is Reproducible

The uploaded document is the source of truth.

Generated artifacts such as:

* embeddings,
* OCR output,
* extracted text caches,

can always be recreated from the original document.

---

# Storage Architecture

```text
React Frontend
        │
        ▼
FastAPI Backend
        │
        ▼
Storage Service
        │
        ▼
Storage Provider Interface
        │
 ┌──────┴──────────────┐
 │                     │
Local Storage      Future Providers
(MVP)             S3 / MinIO / Azure
```

---

# Storage Components

## Storage Service

Responsibilities:

* Save uploaded files
* Read files
* Delete files
* Generate storage paths
* Coordinate duplicate detection

Business services communicate only with the Storage Service.

---

## Storage Provider Interface

Defines a common interface for all storage implementations.

Example responsibilities:

* save()
* read()
* delete()
* exists()

The application should not depend on any provider-specific implementation.

---

## Local Storage Provider (MVP)

Stores files on the local filesystem.

This provider is the default implementation during MVP development.

---

## Future Cloud Providers

Future implementations should satisfy the same interface without requiring changes elsewhere in the application.

---

# Directory Structure

The MVP stores uploaded files using the following hierarchy:

```text
storage/

└── users/
    └── {user_id}/
        └── {workspace_id}/
            └── {document_uuid}.{extension}
```

Example:

```text
storage/

└── users/
    └── 4d4d7.../
        └── 2b81c.../
            └── 8a0d91ef.pdf
```

Benefits:

* Mirrors the domain model.
* Easier debugging.
* Easier manual inspection.
* Simplifies future cleanup.

---

# File Naming Strategy

Physical filenames use UUIDs.

Example:

```text
8a0d91ef-3a4c-4e0c-ae4d-123456789abc.pdf
```

Original filenames are stored in PostgreSQL.

Example:

```text
Operating Systems Notes.pdf
```

Reasons:

* Prevent filename collisions.
* Avoid invalid characters.
* Support document renaming.
* Simplify cloud migration.

---

# Storage Metadata

Each document record stores:

* storage_provider
* storage_path
* original_filename
* mime_type
* file_size

Example:

```text
storage_provider = local

storage_path =
users/{user_id}/{workspace_id}/{uuid}.pdf
```

Future providers may use:

```text
storage_provider = s3
storage_provider = minio
```

---

# File Upload Lifecycle

```text
User Upload
      │
      ▼
Temporary Storage
      │
      ▼
Validate File
      │
      ▼
Calculate SHA-256 Hash
      │
      ▼
Duplicate Detection
      │
      ▼
Move to Permanent Storage
      │
      ▼
Create Database Record
      │
      ▼
Create Background Processing Job
      │
      ▼
Delete Temporary File
```

---

# Temporary Storage

Uploaded files are first written to a temporary location.

Temporary storage exists only for:

* validation,
* duplicate detection,
* upload completion.

Files are moved to permanent storage only after validation succeeds.

Temporary files should always be removed after processing.

---

# Duplicate Detection

Duplicate detection uses SHA-256 hashes.

Workflow:

```text
Upload
    │
    ▼
Calculate SHA-256
    │
    ▼
Compare Hash
Within Same Workspace
    │
    ▼
Duplicate?
```

If a duplicate exists:

* notify the user,
* allow upload to continue,
* create a new document if confirmed.

Duplicate uploads are warnings rather than errors.

---

# File Validation

Before permanent storage:

Validate:

* supported file type,
* file size,
* file integrity,
* upload completion.

Unsupported or corrupted files should never enter permanent storage.

---

# File Retrieval

Document retrieval follows:

```text
Document ID
      │
      ▼
Load Metadata
      │
      ▼
Determine Storage Provider
      │
      ▼
Retrieve Physical File
```

Business services never access storage directly.

---

# File Deletion

Deleting a document performs:

```text
Delete Database Metadata
        │
Delete Physical File
        │
Delete Embeddings
        │
Delete Chunks
        │
Delete Citations
        │
Delete Processing Jobs
```

No orphaned resources should remain.

---

# Workspace Deletion

Deleting a workspace removes:

* uploaded files,
* documents,
* processing jobs,
* chunks,
* embeddings,
* chats,
* citations.

Storage cleanup should occur before the workspace is permanently removed.

---

# Backup Strategy

| Component       | Backup Required | Reason                                 |
| --------------- | --------------- | -------------------------------------- |
| PostgreSQL      | Yes             | Source of truth for metadata           |
| Uploaded Files  | Yes             | Original documents cannot be recreated |
| Local Storage   | Yes             | Contains user-owned content            |
| Qdrant          | Optional        | Can be rebuilt                         |
| Embeddings      | Optional        | Regeneratable                          |
| Temporary Files | No              | Disposable                             |

---

# Storage Provider Abstraction

All storage providers should expose a common interface.

Conceptually:

```text
StorageProvider

save()

read()

delete()

exists()
```

Future providers should require no changes to business services.

---

# Security Considerations

## Access Control

Users may access only their own uploaded files.

Authorization must occur before any file is retrieved.

---

## Path Traversal Protection

The application must never trust user-provided file paths.

All paths should be generated internally.

---

## File Validation

Reject:

* unsupported file types,
* oversized files,
* corrupted uploads.

---

## Storage Isolation

Documents from different users should remain isolated.

The directory hierarchy naturally supports this separation.

---

# Error Handling

Possible failures include:

* storage unavailable,
* insufficient disk space,
* duplicate detection failure,
* file corruption,
* deletion failure.

The system should:

* preserve metadata when appropriate,
* log failures,
* allow retries where possible.

---

# Future Enhancements

Future versions may support:

* Amazon S3
* MinIO
* Azure Blob Storage
* Google Cloud Storage
* Storage encryption at rest
* Versioned documents
* Automatic archival
* Lifecycle policies
* Cross-region backups

These features should not require changes to business logic because of the Storage Provider abstraction.

---

# Design Rationale

| Decision                             | Rationale                                              |
| ------------------------------------ | ------------------------------------------------------ |
| Storage Provider Interface           | Decouples business logic from storage implementation   |
| Local Filesystem for MVP             | Simple, inexpensive, easy to debug                     |
| UUID Filenames                       | Prevent collisions and simplify management             |
| User → Workspace Directory Structure | Mirrors the domain model and aids debugging            |
| SHA-256 Duplicate Detection          | Reliable duplicate detection independent of filename   |
| Temporary Upload Directory           | Prevents incomplete uploads entering permanent storage |
| Uploaded Files as Source of Truth    | Derived artifacts can always be regenerated            |

---

# Implementation Notes

Implementation should follow this design unless a superior approach is identified during development.

If implementation introduces significant architectural changes, this document should be updated to remain the project's source of truth.

---

# Status

**Accepted**

This document should be reviewed whenever:

* new storage providers are added,
* deployment architecture changes,
* backup strategy changes,
* storage requirements evolve,
* document lifecycle requirements change.
