# <Module name> design

[简体中文模板](DESIGN_TEMPLATE.zh-CN.md) · [Documentation](../README.md)

> **Template instructions (remove when finalizing):** Use this file before implementation to explain what the module will build, how it works and how it will be accepted. Keep the overview readable without knowing the algorithm. Put detailed equations, long code snippets and protocol fields in dedicated documents. Replace all placeholders; remove sections that do not apply. A useful first draft is usually 1–3 pages, excluding detailed appendices.

**Design status:** Draft / Reviewed  
**Implementation status:** Not started / In progress / Implemented / Verified  
**Target milestone:** <P1 / P2 / P3 or issue link>  
**Related interfaces:** <links under docs/interfaces/>

## 1. Goal and scope

In a short paragraph, explain the problem this module solves and the value it provides in AfterRec. A reader should be able to answer: *What can the system do once this module is finished?*

- **In scope for this iteration:** <2–5 deliverable capabilities>
- **Out of scope / later:** <explicit exclusions to prevent scope creep>
- **Current basis:** <existing code, demo or verified experiment, with a link; distinguish local evidence from repository integration>

## 2. Overall workflow

Show **one simple diagram** or a numbered sequence with roughly 3–6 steps:

`Input → main processing → output`

Then explain, in ordinary language:
1. What triggers the module?
2. What data or model does it receive?
3. What happens inside the module?
4. What does it return or save?

Include **one small, concrete example** (real or clearly marked illustrative) that makes the flow easy to follow. Keep complex implementation details out of this section.

## 3. Core features and design decisions

For each important feature, write a short subsection covering:
- The expected behavior.
- The selected approach and why it fits the first release.
- The important constraints or trade-offs.

Describe the **current target design**, not every method that might be added someday. For complex algorithms, provide a short overview and link to a separate method document. Label experimental choices and unsupported model/method combinations as pending verification.

## 4. Module boundaries and dependencies

State what this module **owns** and what other modules **own**. For each dependency, say:
- Who provides the input?
- What is exchanged?
- What consumes the output?
- Which interface document defines it?

Link to the applicable [shared contracts](../contracts/INTERFACES.md) and [interface specifications](../README.md#interfaces). Do not redefine schemas in this document. Mark proposed interface changes as **proposed** until both sides agree.

## 5. Rules and failure behavior

List only the constraints that could change the correctness of the implementation: data validity, leakage prevention, model compatibility, error handling, cancellation, reproducibility and synthetic/real-data distinctions, as applicable.

Explain what happens when input is invalid or a dependency fails. Avoid implementation trivia that does not influence behavior.

## 6. Acceptance and verification

Describe observable checks, not vague goals such as "works correctly".

| Check | Input / condition | Expected evidence |
| --- | --- | --- |
| Main flow | <small reproducible example> | <saved result, API response or artifact> |
| Invalid / boundary case | <missing ID, incompatible model, empty data, etc.> | <defined failure behavior> |
| Integration | <real upstream/downstream modules> | <end-to-end output and test> |

State which checks have **actually passed**, where the evidence lives, and which still need to run. A mock demo is not proof that a real training or unlearning pipeline works.

## 7. Open decisions and references

Before implementation begins, list unresolved questions that affect **scope, input/output or acceptance** and record the agreed decisions. Do not hide essential decisions inside long technical notes.

Link to detailed algorithm notes, tests, papers, external code and applicable licenses when used. Public architecture pages can remain framework-neutral, but source attribution and license compliance must remain accurate.

---

**Ready-to-build review:** The goal and exclusions are clear; the workflow can be understood quickly; module dependencies have agreed interfaces; acceptance checks are testable; planned work and completed evidence are distinguished.
