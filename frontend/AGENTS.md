# Web prototype and frontend (Student C)

- `index.html` is an offline demo; every dataset, metric and trajectory shown there
  is synthetic. Keep its visible demo disclaimer during changes.
- Do not call a mock endpoint or fabricated score a production experiment result.
- Use shared API contracts; coordinate input/output changes with A and B.
- Prefer a simple, accessible, responsive interface. Do not add frontend tooling
  or large dependencies without an issue and an explicit migration plan.
- Run `python scripts/check_frontend.py` after editing the static prototype.
