# Agent simulation runtime

- This folder owns execution infrastructure and pluggable agent policies.
- Document and test changes to persona construction, memory semantics or perceived-association metrics in the research protocol.
- Pass forgetting intent to the simulated user agent, not the recommender in the
  data-unlearning-only condition.
- Agent can act only on exposed items. Reject invalid action targets.
- No future observations, ground-truth labels or post-hoc outcomes in prompts.
- Start each Original/Retrain/Unlearned simulation arm with fresh state.
- Freeze model parameters. Use identical session feedback logic in each arm.
- Mark fixtures as synthetic, and never equate agent rationale with human truth.
