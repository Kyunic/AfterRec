# <Provider> and <Consumer> interface

[简体中文](INTERFACE_TEMPLATE.zh-CN.md) · [Documentation](../README.md)

> Instructions (remove after copying into an interface document): Use this template only when two modules, or the frontend and backend, need to agree on a new call or data format. The aim is a shared understanding of what to call, what to send and what comes back. Link existing types from the [shared contracts](../contracts/INTERFACES.md) instead of redefining them. The two sections below are sufficient for most interfaces.

**Interface status:** Proposed / Agreed by both sides

## 1. Use case

In a few sentences, say when the interface is used, who provides it and who consumes it.

- **Provider:** <module or service>
- **Consumer:** <module or page>
- **Purpose:** <for example, start an unlearning task and obtain its model reference>

## 2. Operation and input/output

| Operation or artifact | Input | Output |
| --- | --- | --- |
| <Python function / HTTP method and path / file artifact> | <required arguments or data type> | <response or artifact> |

State the call style (function, HTTP or file) and explain fields that affect integration. Reuse existing types by reference. Describe new or ambiguous fields only, and add a minimal input/output example if useful.

**Only if relevant:** Specify asynchronous job states, error responses, ID/version rules, cancellation or retries when the consumer depends on them. Do not fill out error matrices or integration-test checklists by default.

Both sides should agree on this contract before implementing independently. Changes to shared fields should update affected documentation and code together.
