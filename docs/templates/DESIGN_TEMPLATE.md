# <Module name> design

[简体中文](DESIGN_TEMPLATE.zh-CN.md) · [Documentation](../README.md)

> Instructions (remove after copying into a module DESIGN.md): This is a short pre-development plan. It should tell contributors and maintainers what will be built in the current iteration, how it will work and what the finished feature will do. Keep the four sections below. Prefer short prose and one simple diagram. Put detailed algorithms, parameters and code in a separate technical note. Delete anything that adds no useful information.

**Design status:** Draft / Agreed

## 1. Goal and scope

In two or three sentences, explain the problem this module addresses and what the current iteration will deliver.

- **In scope:** <concrete capabilities, usually 2–4>
- **Out of scope (only if likely to be misunderstood):** <work explicitly deferred>

## 2. Workflow and approach

Use a simple diagram or a few steps:

`Input → main processing → output`

Explain how the main functions fit together, which implementation approach is proposed and why it fits this iteration. Focus on the actual flow instead of listing every possible method. Add one small example if it makes a difficult step clearer. Link to separate notes for algorithm derivations or implementation details.

## 3. Dependencies and handoffs

Explain what this module needs from others and what it provides to downstream modules.

- **Inputs and dependencies:** <module, data or capability>
- **Outputs:** <result and its consumer>
- **Interface specification:** <link under `docs/interfaces/`>

Refer to the [shared contracts](../contracts/INTERFACES.md) for existing types and signatures. Describe the handoff here without copying field definitions. If the module has no cross-module dependency, a sentence is sufficient.

## 4. Done for this iteration

List **2–4 observable deliverables**, such as “train a model with the specified data and reload its checkpoint”. Avoid generic statements such as “all features work”.

<What can someone run, inspect or reproduce when this iteration is finished?>

The deliverables should match the scope above. Distinguish mock demos, locally verified work and functionality integrated into the repository.

> **Only when needed:** Add a short note about constraints or decisions that genuinely block implementation, plus relevant references. Do not add mandatory sections for risk registers, integration sign-off, edge-case catalogs or open questions. Credit external implementations and respect their licenses in the relevant technical documentation.
