# ADR 13: Use Transaction-Based Isolation for Integration Tests

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision Type:** Testing / Infrastructure
- **Related:** Backend Foundation, Integration Testing, Database Session Management

---

## Context

The backend requires integration tests that exercise the real PostgreSQL
database and the FastAPI application together.

Using the development database directly would allow test data to persist
between test runs and could cause tests to interfere with development data.

We therefore use a dedicated PostgreSQL database for integration testing.

A second concern is isolation between individual tests. Each test may create,
modify, or delete database records, but those changes should not persist after
the test completes.

The test environment also needs to ensure that database operations performed
by pytest fixtures and database operations performed by FastAPI during the
request use the same database transaction.

Several approaches were considered, including creating independent sessions
for fixtures and API requests and explicitly deleting test data after each
test.

---

## Decision

Integration tests will use a dedicated PostgreSQL test database with
transaction-based isolation.

Each database integration test will:

1. Obtain a connection from the test database engine.
2. Explicitly begin a database transaction.
3. Create an `AsyncSession` bound to that connection.
4. Share the same `AsyncSession` with pytest fixtures and the FastAPI
   database dependency through dependency overriding.
5. Use `flush()` when test fixtures need database-generated values or need
   their changes to be visible within the transaction.
6. Avoid committing test data during the test.
7. Roll back the transaction after the test completes.

The database-session fixture owns the transaction lifecycle.

The resulting relationship is:

```text
Dedicated Test PostgreSQL Database
                ↓
           Test Engine
                ↓
          DB Connection
                ↓
           Transaction
                ↓
           AsyncSession
             ↙      ↘
    Pytest Fixtures  FastAPI Dependency
             ↘      ↙
             Same Transaction
                    ↓
             Test Completion
                    ↓
                Rollback
```

## Rationale

A dedicated test database provides isolation from development data while
still allowing integration tests to exercise the actual PostgreSQL database.

Transaction-based isolation provides a predictable cleanup mechanism without
requiring individual tests to manually delete every record they create.

Sharing the same AsyncSession between pytest fixtures and the FastAPI
dependency is important because both sides must participate in the same
transaction. This allows fixtures to prepare database state that is visible
to the API request while ensuring that the API request's database changes
are also covered by the same rollback.

Using flush() instead of commit() allows test data to be persisted within
the active transaction and allows generated database values to become
available without making the changes permanent.

## Alternatives Considered
1. Use the development database

Rejected.

This would allow integration tests to modify development data and would
create an unacceptable coupling between development and testing.

2. Create an independent database session for each fixture/request

Rejected.

Independent sessions would make transaction ownership unclear and could
result in fixture-created data and API operations participating in different
transactions.

3. Explicitly delete test data after each test

Rejected.

Manual cleanup is more error-prone. A test may create multiple related
records, and forgetting to clean up one of them can cause later tests to
fail.

4. Use transaction rollback

Accepted.

Rollback provides a centralized cleanup mechanism and keeps the database
state isolated between tests while allowing the tests to exercise the real
database.

## Consequences
# Positive
Integration tests cannot modify the development database.
Test data does not persist after a test completes.
Tests can share a single transaction-scoped AsyncSession.
Pytest fixtures and FastAPI requests operate on the same transaction.
Test cleanup is centralized in the database-session fixture.
Tests can use real PostgreSQL behavior instead of a mocked database.
# Negative
Integration tests require a running PostgreSQL test database.
The fixture lifecycle is more complex than creating a normal SQLAlchemy
session.
Tests that require committed data or database behavior that depends on a
committed transaction may require a different testing strategy.
The test environment must keep its database schema synchronized with the
application migrations.

## Implementation Notes

The current implementation uses:

a dedicated PostgreSQL test database;
SQLAlchemy's asynchronous engine;
an explicit connection-level transaction;
a transaction-bound AsyncSession;
FastAPI dependency overrides;
pytest fixtures for database state;
flush() rather than commit() for test data;
rollback during fixture teardown.

The implementation should remain aligned with this decision unless a future
testing requirement demonstrates that another isolation strategy is needed.
