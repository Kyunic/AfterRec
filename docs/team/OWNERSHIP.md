# Team ownership and delivery

| Role | Scope | Accountability |
| --- | --- | --- |
| Research Lead / Project Owner | Scientific questions, platform scope, research agent | Sign off on milestones and experiment claims; not routine code reviews |
| Student A | `datasets/`, `recsys/` | Real RecBole training, reproducible datasets, ID mappings and recommendation interface |
| Student B | `unlearning/`, `evaluation/` | Forget partitions, Retrain implementation, metrics and scientific verification |
| Student C / Integration Lead | `api/`, `frontend/`, integration tooling | Local Web app, task flow, APIs and integration of all modules |
| Shared A+B+C | `core/`, shared contracts, simulation runtime and CI | Coordinate changes via Issues and interface tests |

Student C builds the **simulation runtime**, but the Research Lead owns
scientific decisions about personas, forgetting intent, memory and agent policy.
A/B participate whenever shared scientific interfaces are changed.

## Lightweight weekly process

1. Start of week: maximum 2-3 scoped Issues per student, each with acceptance tests.
2. Each Issue: `feat/<issue-number>-short-description` branch, focused PR.
3. CI and tests run automatically. Agent-assisted review + **peer verification**.
4. Student C integrates; A/B fix faults in their own modules.
5. End of week: show an actual running demonstration and note blockers.
6. Project Owner checks observable results and scientific plausibility; no
   requirement to inspect every implementation line.

## Shared-file change protocol

Before changing shared schemas, `pyproject.toml`, workflows, or `AGENTS.md`:
write in the Issue why it is necessary, which consumers must change and how the
old behavior remains tested; get acknowledgement from the affected students.

Do not enforce GitHub CODEOWNERS until real student usernames are known.
Use `docs/team/CODEOWNERS.example` as a template; enable 1 peer approval +
passing CI when available for the private repository plan.

## Important caveat

AI-generated code, tests and AI reviews can share the same defect. A second
student should independently test the observable behavior and compare any
research algorithm to its actual paper/protocol. No code-free workflow alone
can guarantee numerical correctness.
