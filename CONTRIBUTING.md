# Contributing to RecForgetBench

Development is currently limited to invited collaborators. The repository will
be opened later after a license, data usage policy and reproducibility checks
are agreed upon.

## Workflow

1. Read `AGENTS.md`, `docs/team/OWNERSHIP.md`, `docs/contracts/INTERFACES.md`.
2. Pick one scoped GitHub Issue with an owner and observable acceptance criteria.
3. Create a short-lived branch such as `feat/12-recbole-topk`.
4. Implement the smallest change and test it locally.
5. Submit a Pull Request using the supplied template.
6. Get CI checks + peer verification; let Student C coordinate integration.
7. Do not self-merge untested changes or push directly to `main`.

## Commands

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python scripts/verify_scaffold.py
python scripts/check_frontend.py
ruff check backend tests scripts
```

The current frontend is a dependency-free offline HTML **concept prototype**;
it is not a real recommender frontend. Installing RecBole and downloading data
are separate, opt-in steps managed by Student A.

## PR quality gate

- Evidence of real functionality, not only generated code.
- Tests that fail for incorrect behavior.
- Examples with honest data provenance.
- No secrets, private user records, checkpoints or bulk datasets.
- A second student independently verifies affected scientific outputs.
- Shared interfaces and module boundaries remain compatible.

## License status

There is currently **no public license** for this repository. Do not assume
permission to redistribute the source or attached third-party datasets. The
Project Owner will select a license before publication.
