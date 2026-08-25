\# ADR-002: Workspace-Based Knowledge Organization



\## Status



Accepted



\---



\## Context



Documents need to be organized in a way that matches how students naturally think about their academic materials.



\---



\## Decision



Knowledge will be organized into Workspaces.



A workspace represents a subject, course, semester, project, or learning area.



Each workspace contains:



\* documents,

\* chats,

\* summaries,

\* generated study aids.



\---



\## Example



Workspace: Operating Systems



\* Notes.pdf

\* Book.pdf

\* PPTs

\* Chats



\---



\## Search Strategy



\### MVP



Search within a single workspace.



\### Future



Allow searching across multiple selected workspaces.



\---



\## Alternatives Considered



\### One Document = One Chat



Rejected because it scales poorly.



\### Automatic Workspace Linking



Rejected because it may produce unpredictable retrieval behavior.



\### User-Selected Multi-Workspace Search



Accepted for future phases.



\---



\## Consequences



\### Positive



\* Better organization.

\* More natural user experience.

\* Easier permission management.

\* Easier future collaboration features.



\### Negative



\* Requires workspace management features.

\* Adds additional database entities.



