# Assumptions

## Purpose

This document captures the assumptions made during product discovery and requirements engineering for the Student Study Assistant platform.

These assumptions define the conditions under which the requirements, architecture, and product decisions are considered valid.

If any of these assumptions prove to be incorrect, the product requirements, architecture, and roadmap may need to be revisited.

---

# Product Assumptions

## PA-1

Students struggle more with information overload and organization than with the lack of study material.

### Rationale

Most students already have access to large amounts of content but struggle to determine:

* what to study,
* how deeply to study,
* where to find information.

---

## PA-2

Students value learning efficiency more than unlimited information generation.

### Rationale

Most students study under time constraints and prioritize exam performance and efficient revision.

---

## PA-3

Students prefer an AI assistant that works with their own study materials rather than a generic AI assistant.

---

## PA-4

Personalization provides meaningful value and differentiates the platform from generic AI tools.

---

## PA-5

Students naturally organize their academic materials subject-wise.

### Implication

The primary organizational unit of the platform will be a subject-based workspace.

---

# User Assumptions

## UA-1

The primary users of the MVP are university students.

---

## UA-2

Target users possess basic digital literacy and are comfortable using web applications.

---

## UA-3

Target users already use digital study materials.

Examples:

* PDFs
* PPTs
* Lecture notes
* Previous year papers
* Online resources

---

## UA-4

Users are willing to upload their academic materials to obtain personalized assistance.

---

## UA-5

Users are willing to create and manage subject-based workspaces.

---

## UA-6

Users are willing to interact with AI to support their learning process.

---

## UA-7

Users are comfortable with AI-generated responses as long as the responses are grounded in their study materials.

---

## UA-8

Most users study multiple subjects simultaneously.

---

## UA-9

Users frequently prepare for examinations under limited time constraints.

---

# Educational Assumptions

## EA-1

Syllabus boundaries influence how deeply students want to learn a topic.

---

## EA-2

Students benefit from explanations tailored to their syllabus and assessment context.

---

## EA-3

Previous papers and assessment materials provide useful signals about topic importance and examination expectations.

---

## EA-4

Students prefer concise, exam-relevant answers by default and request deeper explanations only when necessary.

---

## EA-5

Reducing context switching improves learning productivity.

---

## EA-6

Many users will upload syllabus documents and assessment materials when they understand the benefits of personalized learning.

---

## EA-7

The platform must remain useful even when syllabus documents are not provided.

In the absence of syllabus information, the platform should continue providing contextual but generic assistance.

---

# Technical Assumptions

## TA-1

Most uploaded documents contain machine-readable text or printed text that can be extracted through OCR technologies.

---

## TA-2

A significant portion of academic documents contain scanned pages or image-based text and therefore require OCR support.

---

## TA-3

Document extraction quality will be sufficient for meaningful retrieval and question answering.

---

## TA-4

Semantic embeddings can effectively represent academic content.

---

## TA-5

Retrieval-Augmented Generation (RAG) can significantly reduce hallucinations compared to standalone LLM responses.

---

## TA-6

A workspace-scoped retrieval approach is sufficient for validating the MVP.

---

## TA-7

Single-workspace search will satisfy most user queries during the MVP stage.

---

## TA-8

User preferences and chat history can improve response quality and personalization.

---

## TA-9

The platform should support both online and offline deployment models depending on the selected AI provider.

---

## TA-10

Internet connectivity is required only when cloud-based AI providers or external APIs are used.

Local AI deployments should remain functional without internet access.

---

## TA-11

The majority of uploaded study materials will be:

* text PDFs,
* scanned PDFs,
* PNG or JPG images containing printed text.

---

## TA-12

Handwritten notes, diagrams, and highly visual documents are not primary document types for the MVP and may not be fully supported.

---

# Business Assumptions

## BA-1

University students experience this problem frequently enough to validate the product.

---

## BA-2

Students are willing to adopt a new learning tool if it saves time and improves study efficiency.

---

## BA-3

There is sufficient differentiation between this platform and generic AI assistants.

---

## BA-4

Students are price-sensitive and benefit from affordable AI options such as local models and bring-your-own-key support.

---

## BA-5

Positive learning outcomes will lead to repeat usage and long-term retention.

---

# Data Assumptions

## DA-1

Users retain ownership of their uploaded study materials.

---

## DA-2

Users expect their study materials and conversations to remain private.

---

## DA-3

Users may upload incomplete, inconsistent, low-quality, or poorly formatted documents.

---

## DA-4

The system must tolerate varying document quality and still provide useful assistance.

---

## DA-5

Different document formats and extraction methods can be normalized into a common representation for indexing and retrieval.

---

# Future Assumptions

## FA-1

Future user segments such as competitive exam aspirants, researchers, teachers, and professionals can be supported without major redesign of the core platform.

---

## FA-2

Advanced learning features such as quizzes, analytics, adaptive tutoring, and study planning can be layered on top of the MVP architecture.

---

# Assumptions Requiring Validation During MVP

The following assumptions should be validated through user testing and feedback:

1. Students are willing to upload study materials.
2. Subject-based workspaces match user expectations.
3. Personalized learning assistance improves user satisfaction.
4. Syllabus-aware responses provide measurable value.
5. Users return regularly to the platform.
6. The platform reduces time spent searching and organizing information.
7. OCR quality is sufficient for academic documents.
8. Students perceive meaningful value over existing workflows such as:

   * ChatGPT
   * NotebookLM
   * PDFs
   * WhatsApp groups
   * Traditional note-taking applications.

---

# Revision Policy

This document should be revisited whenever:

* user research invalidates an assumption,
* major architectural changes are introduced,
* new target user segments are added,
* product strategy changes significantly.
