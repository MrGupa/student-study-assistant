# ADR-012: Learning Efficiency First Principle

## Status

Accepted

---

## Context

User research revealed that students do not primarily struggle because study materials are unavailable.

The primary challenges are:

* Too much information to process.
* Limited preparation time before examinations.
* Difficulty determining what topics are important.
* Difficulty understanding how deeply a topic needs to be studied.
* Generic AI tools that do not understand educational context.

Most students optimize their studying to maximize learning outcomes and examination performance within limited time constraints.

Therefore, the product should not focus on helping students consume more information, but rather on helping them learn more efficiently.

---

## Decision

The platform will adopt a **Learning Efficiency First** principle.

The product will prioritize features that help students:

1. Learn the right topics.
2. Learn topics at the appropriate depth.
3. Prioritize high-value content.
4. Reduce time spent searching and organizing information.
5. Maximize learning outcomes within limited preparation time.

The platform will optimize for:

> Learning Efficiency

rather than:

> Maximum Content Consumption.

---

## Product Principle

Help students learn the right things at the right depth within their limited time.

---

## Implications

This principle influences product decisions across all areas of the platform.

### Prioritize

* Syllabus-aware learning
* Topic importance detection
* Previous paper analysis
* Efficient revision workflows
* Information retrieval
* Personalized learning context
* Exam-oriented study support
* Knowledge organization

### Deprioritize

* Generic tutoring features
* Unlimited content generation
* Features that increase information overload
* Features that do not improve learning efficiency

---

## Rationale

Students often prepare under time constraints and are primarily concerned with:

* What should I study?
* What can I skip?
* How deeply should I study this topic?
* What gives me the highest learning value?

Helping students answer these questions provides significantly more value than simply generating additional information.

---

## Consequences

### Positive

* Strong product differentiation.
* Clear feature prioritization.
* Better alignment with real student behavior.
* Reduced feature creep.
* Stronger support for exam-oriented learning workflows.
* Easier prioritization of MVP features.

### Negative

* Some advanced tutoring capabilities become lower priority.
* Certain power-user features may be postponed.
* Educational outcomes may require additional metrics and user feedback to measure.

---

## Alternatives Considered

### Option 1: Generic AI Study Assistant

Provide answers and content generation without educational context.

**Rejected** because it offers limited differentiation and does not address the core user problems.

---

### Option 2: Learning Efficiency First Platform

Optimize for helping students learn efficiently and make better study decisions.

**Accepted** because it directly addresses the identified pain points and aligns with the product vision.

---

## Related ADRs

* ADR-001: Product Vision and Scope
* ADR-003: Personalized Learning Memory
* ADR-006: Syllabus-Aware Learning
* ADR-009: Problem Prioritization
* ADR-010: Product Success Definition
* ADR-011: Product Differentiation Strategy
