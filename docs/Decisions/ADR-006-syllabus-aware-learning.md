# ADR-006: Syllabus-Aware Learning

## Status

Accepted

---

## Context

Students often struggle to determine:

* what topics are important,
* how deeply a topic should be studied,
* what falls within the boundaries of their syllabus.

Generic AI systems provide broad answers that may exceed the user's requirements.

---

## Decision

The platform will support Syllabus-Aware Learning.

Users may optionally upload:

* syllabus documents,
* previous year papers,
* assessment materials.

The system will use these resources to tailor explanations according to the user's educational context.

---

## Default Behavior

AI responses should remain within syllabus boundaries.

Users may explicitly request deeper explanations.

---

## Consequences

### Positive

* Better learning efficiency.
* Reduced information overload.
* Strong product differentiation.
* Improved exam preparation.

### Negative

* Additional ingestion complexity.
* Metadata extraction requirements.
* Increased prompt engineering complexity.

---

## Alternatives Considered

### Generic RAG Responses

Rejected because they often provide too much information and do not align with educational requirements.

### Mandatory Syllabus Upload

Rejected because it increases onboarding friction.

### Optional Advanced Mode

Accepted.
