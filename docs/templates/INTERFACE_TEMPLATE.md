# <Provider> ↔ <Consumer> interface

[简体中文模板](INTERFACE_TEMPLATE.zh-CN.md) · [Documentation](../README.md)

> **Template instructions (remove when finalizing):** Agree on this contract **before separate modules are implemented**. Use it for Python module boundaries, HTTP frontend/backend APIs or persisted artifacts. Specify only what the current milestone needs. Reuse existing types from [shared contracts](../contracts/INTERFACES.md); do not create a competing definition.

**Status:** Proposed / Agreed / Implemented / Verified  
**Protocol version:** <e.g., v0.1>  
**Related design documents:** <links>  
**Scope:** <feature or scenario covered>

## 1. Purpose and boundary

In 2–4 sentences, say what the consumer needs, which module provides it and what this contract does **not** cover.

**Producer:** <module or service>  
**Consumer:** <module or web page>  
**When used:** <trigger in the overall flow>

## 2. Operations and data flow

For each operation, record the **direction**, **name or route**, **inputs**, **outputs**, and whether it is synchronous, asynchronous or file-based. Include only operations required for the first working integration.

| Direction | Operation (function / HTTP method + path / artifact) | Request or input | Response or output |
| --- | --- | --- | --- |
| <A → B> | <name> | <type/reference> | <type/reference> |

For a background job, explain how to obtain the **run ID, state, result and failure reason**. For frontend/backend APIs, specify polling or event delivery only if it is part of the agreed design.

## 3. Data contract

Link existing objects in [INTERFACES.md](../contracts/INTERFACES.md). Define **only new or changed fields** here.

| Field | Type | Required? | Meaning and validation |
| --- | --- | --- | --- |
| <field> | <type> | <yes/no> | <semantics, allowed values, defaults> |

Clarify identifiers and mappings, versions, units, nullable fields, ordering and file formats where relevant. Include **one small valid request/response or input/output example** based on the agreed schema. Clearly label illustrative examples; never present a proposed endpoint as already implemented.

## 4. Errors and lifecycle

Describe the cases both sides must handle: missing or incompatible inputs, invalid IDs, malformed payloads, timeouts, cancellation, partial results and retries. State any idempotency or duplicate-request rules.

For HTTP, include status codes and error-body examples. For Python calls, define raised exceptions or structured errors. For persisted artifacts, state when a file is considered complete and safe to consume.

## 5. Integration checks

Provide 2–4 verifiable cases:
- A valid request produces the documented output.
- Invalid input produces a defined response.
- The consumer can use the output **without knowing the provider's internal code**.
- If applicable, cancellation/retry or version mismatch behaves as agreed.

Record links to schema tests and the first real cross-module integration test. Distinguish planned checks from passing checks.

## 6. Decisions and change control

List open questions that block integration. The producer and consumer should agree on required fields and lifecycle behavior before either side depends on them. When updating a shared contract, update affected code, tests and [INTERFACES.md](../contracts/INTERFACES.md) in the same change. Document incompatible revisions and migration rules.

---

**Ready-for-integration review:** Both sides know what to call, what to send, what to expect, how failure is reported and how the contract will be tested.
