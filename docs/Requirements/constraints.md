# Constraints

## Purpose

This document defines the constraints under which the Student Study Assistant platform will be designed, developed, and operated.

Constraints represent limitations that influence product decisions, architecture, implementation, and roadmap planning.

---

# Business Constraints

## BC-1

The product is being developed by a small team with limited engineering resources.

### Implication

The MVP must remain narrowly scoped and avoid unnecessary complexity.

---

## BC-2

The primary goal of the MVP is product validation rather than feature completeness.

### Implication

Features that do not directly validate the core value proposition should be deferred.

---

## BC-3

Target users are price-sensitive students.

### Implication

The platform should support affordable AI options and avoid excessive infrastructure costs.

---

## BC-4

The product must clearly differentiate itself from generic AI assistants.

### Implication

Features should prioritize:

* personalization,
* syllabus awareness,
* learning efficiency,
* workspace organization.

---

# Product Constraints

## PC-1

The MVP is focused exclusively on university students.

Other user segments are outside the MVP scope.

---

## PC-2

The primary organizational unit of the platform is a subject-based workspace.

---

## PC-3

The MVP supports search only within a single workspace.

Cross-workspace search is outside the MVP scope.

---

## PC-4

The MVP does not support collaboration features.

---

## PC-5

The following features are outside the MVP scope:

* Quizzes
* Flashcards
* Learning analytics
* Study plans
* Adaptive tutoring
* Exam simulations

---

## PC-6

The platform prioritizes learning efficiency over maximum content generation.

---

## PC-7

Syllabus upload is optional and cannot be required during onboarding.

---

## PC-8

The platform must remain useful even when syllabus documents are unavailable.

---

## PC-9

The MVP will be delivered as a web application.

Desktop and local-first deployments are future considerations.

---

# User Constraints

## UC-1

Students have limited preparation time and expect quick access to information.

---

## UC-2

Students may upload incomplete, inconsistent, or low-quality study materials.

---

## UC-3

Students may have limited knowledge of AI systems and configuration.

---

## UC-4

Students may use the platform irregularly and primarily during examinations and revision periods.

---

## UC-5

Students expect minimal onboarding friction and simple workflows.

---

# Technical Constraints

## TC-1

The system must support future deployment models that include:

* cloud-hosted AI,
* bring-your-own-key (BYOK),
* local AI providers.

---

## TC-2

The system cannot assume continuous internet connectivity.

Internet access may not be available in local deployment scenarios.

---

## TC-3

The quality of retrieval depends heavily on document quality and extraction accuracy.

---

## TC-4

OCR quality may vary depending on:

* scan quality,
* image resolution,
* document formatting.

---

## TC-5

The MVP supports the following document types:

* Text PDFs
* Scanned PDFs
* PNG images containing printed text
* JPG images containing printed text

---

## TC-6

The MVP does not guarantee support for:

* Handwritten notes
* Mathematical equations
* Complex diagrams
* Low-quality photographs
* Highly visual documents

---

## TC-7

The system must operate within the context limitations of the selected language model.

---

## TC-8

The system cannot guarantee perfect retrieval accuracy or zero hallucinations.

---

## TC-9

AI responses depend on the quality and completeness of uploaded materials.

---

## TC-10

Large document collections may increase:

* indexing time,
* storage requirements,
* response latency.

---

## TC-11

The architecture must support future growth without major redesign.

---

## TC-12

The architecture should abstract:

* document storage,
* vector storage,
* AI providers,

to enable future local-first deployments.

---

## TC-13

The system should be deployable on commodity hardware for local development and future self-hosted deployments.

---

# Data Constraints

## DC-1

Uploaded documents may contain:

* duplicate information,
* contradictory information,
* outdated information,
* missing information.

---

## DC-2

The platform cannot guarantee the correctness of user-provided content.

---

## DC-3

Different document formats require normalization before indexing and retrieval.

---

## DC-4

Large documents and document collections may increase processing time and operational cost.

---

## DC-5

The system should avoid unnecessary duplication of user files and derived artifacts.

---

# AI and Model Constraints

## AC-1

Large language models may generate incorrect or misleading responses.

---

## AC-2

Embedding models may fail to capture certain educational nuances.

---

## AC-3

Model performance may vary significantly between:

* cloud-hosted models,
* local models,
* different providers.

---

## AC-4

The quality of personalization is limited by the amount of historical user data available.

---

## AC-5

The system cannot guarantee that every answer perfectly aligns with examination expectations.

---

## AC-6

The platform cannot guarantee that every retrieved source is relevant.

---

# Legal and Privacy Constraints

## LC-1

Users retain ownership of their uploaded materials.

---

## LC-2

User documents and conversations must remain private.

---

## LC-3

The platform may store copyrighted educational materials uploaded by users.

The system must avoid unauthorized distribution of these materials.

---

## LC-4

The platform must comply with applicable privacy and data protection regulations.

---

## LC-5

The platform should minimize the amount of user data stored whenever possible.

---

# Operational Constraints

## OC-1

Document processing time depends on:

* file size,
* OCR requirements,
* system load.

---

## OC-2

AI response latency depends on:

* model size,
* infrastructure,
* retrieval complexity,
* provider limitations.

---

## OC-3

External AI providers may impose:

* rate limits,
* token limits,
* pricing constraints,
* availability constraints.

---

## OC-4

Local models may require significant computational resources and may not perform equally across devices.

---

## OC-5

Cloud infrastructure costs must remain sustainable during MVP validation.

---

# Future Constraints

## FC-1

Future features should not require redesign of the core User model.

---

## FC-2

Future features should not require redesign of the Workspace model.

---

## FC-3

Future expansion should preserve backward compatibility with existing user data whenever possible.

---

## FC-4

Architectural decisions made during the MVP should allow future support for:

* Cross-workspace search
* Collaboration
* Quizzes
* Learning analytics
* Adaptive learning
* Study plans
* Desktop applications
* Local-first deployments
---

## FC-5

The MVP shall not implement local-first storage or desktop clients, but the architecture should avoid decisions that would prevent future support.

---

# Constraint Review Policy

This document should be reviewed whenever:

* major product scope changes occur,
* new target users are introduced,
* significant technical limitations are discovered,
* infrastructure strategy changes,
* deployment strategy changes.
