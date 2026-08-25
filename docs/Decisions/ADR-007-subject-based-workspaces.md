# ADR-007: Subject-Based Workspace Organization

## Status

Accepted

---

## Context

Students naturally organize their studies by subject.

Assignments, revision, and examinations are also typically subject-specific.

---

## Decision

The primary organizational unit of the platform will be:

Workspace = Subject

Examples:

* Operating Systems
* Database Management Systems
* Computer Networks

---

## Search Strategy

### MVP

Search only within a workspace.

### Future

* Workspace Groups
* Multi-Workspace Search
* Global Search

---

## Consequences

### Positive

* Matches user mental model.
* Simpler navigation.
* Easier retrieval.
* Easier syllabus integration.

### Negative

* Interdisciplinary queries become harder.
* Future cross-workspace search requires additional engineering.

---

## Future Consideration

The architecture should allow the introduction of Workspace Groups without major schema redesign.
