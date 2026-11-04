# Agent runtime (Student C + Research Lead)

- This folder owns execution infrastructure, NOT new scientific agent algorithms.
- Do not change persona construction, psychology, memory semantics, or residual-
  association metrics without approval from the Research Lead.
- Pass forgetting intent to the simulated user agent, not the recommender in the
  data-unlearning-only condition.
- Agent can act only on exposed items. Reject invalid action targets.
- No future observations, ground-truth labels or post-hoc outcomes in prompts.
- Start each Original/Retrain/Unlearned simulation arm with fresh state.
- Freeze model parameters. Use identical session feedback logic in each arm.
- Mark fixtures as synthetic, and never equate agent rationale with human truth.
