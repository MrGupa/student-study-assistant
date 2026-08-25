# ADR-008: Generic User Model

## Status

Accepted

---

## Context

The platform serves multiple personas:

* Students
* Competitive Exam Aspirants
* Researchers
* Teachers

Many users may belong to more than one persona simultaneously.

---

## Decision

The platform will use a single generic User model.

Personas will be used for product design and feature prioritization rather than authorization.

---

## Rationale

The functional differences between personas do not justify separate user roles or dashboards.

---

## Consequences

### Positive

* Simpler authentication.
* Simpler onboarding.
* Flexible future expansion.
* Supports multi-role users.

### Negative

* Future permission systems may require additional metadata.

---

## Alternatives Considered

### Separate Student and Teacher Roles

Rejected because it introduces unnecessary complexity and does not provide sufficient benefits.

### Generic User Model

Accepted.
