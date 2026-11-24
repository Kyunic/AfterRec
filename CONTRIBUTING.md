# Contributing to AfterRec

Thanks for your interest in AfterRec. We welcome focused bug reports, reproducibility fixes, documentation improvements and proposals for new recommendation, unlearning or simulation adapters.

## Before contributing

Read the [README](README.md), [architecture](docs/architecture/OVERVIEW.md), [shared interfaces](docs/contracts/INTERFACES.md) and [simulation protocol](docs/research/SIMULATION_PROTOCOL.md). Check existing Issues before proposing a change.

For new modules or cross-module changes, use the [design template](docs/templates/DESIGN_TEMPLATE.md) and [interface template](docs/templates/INTERFACE_TEMPLATE.md) to agree on scope, observable acceptance criteria and module boundaries before implementation. The corresponding [Chinese templates](docs/templates/DESIGN_TEMPLATE.zh-CN.md) and [interface template](docs/templates/INTERFACE_TEMPLATE.zh-CN.md) are also available.

## Development workflow

1. Open or select an Issue with a clear scope and acceptance criteria.
2. Create a short-lived branch (for example, `feat/12-recommend-topk`).
3. Keep implementation changes within the relevant module. Discuss contract changes first.
4. Add tests, including failure cases for data or evaluation changes.
5. Open a Pull Request explaining behavior, actual test results, limitations and any new dependencies.
6. Use CI and independent verification for research-critical outputs.

For the current Python scaffold:

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
python scripts/verify_scaffold.py
python scripts/check_frontend.py
```

## Research quality

Keep Original, fresh Retrain and Unlearned results distinct. Report dataset and split provenance, candidate protocols, random seeds and model versions. Label synthetic examples explicitly; a passing test or simulated interaction does not establish real-world human validity. Avoid committing private data, credentials, bulk datasets or model weights.

## Licensing

This repository has not yet adopted a software license. Public visibility does not by itself grant redistribution or modification rights; check applicable permissions before reusing code. External datasets and dependencies have separate terms.
