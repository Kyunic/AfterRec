# Simulation research boundary & evaluation protocol

## Research question

When an interaction is deleted from a recommender's training set, what residual
associations can a user still perceive during repeated recommendation exposure,
and how reliably can a simulated user detect these effects?

This asks a different question from whether training data influence has been
technically removed. The project must not conflate the two.

## Simulation observation boundary

- The user agent can see only an approved persona, its own forgetting intent,
  current displayed items, and prior executed interactions.
- The base recommender receives user ID and prior session feedback. It does
  **not** receive the semantic forgetting intent in data-unlearning-only mode.
- Neither agent nor recommender receives held-out future actions, hidden human
  judgments, evaluation labels, or reference-model outcomes.
- Any LLM output is a *simulated* action or judgment, not a real human observation.
- Actions must use displayed items only and conform to a fixed action schema.

## Controlled model-arm comparisons

1. Original / Retrain / Unlearned use the same eligible users and catalog.
2. Reset the simulation agent's memory and session state for each arm.
3. Use the same feedback-adapter code and parameters for all arms.
4. Freeze recommendation model parameters throughout a rollout.
5. Log the base recommendation scores separately from session re-ranking.
6. Repeat randomized agent runs; record prompts/model versions and uncertainty.
7. Never claim that repeated exposure implies failed technical data deletion.

## Evaluation layers (not yet implemented)

- Technical unlearning diagnostics: retrain gap, privacy-attack indicators,
  retained utility and runtime.
- Perceived association: direct, indirect-semantic, contextual or unrelated
  exposure. Explicitly retain an *uncertain* label.
- Trajectory: first exposure, repeat exposure, after-dislike exposure, exit.
- Simulator validity: action validity, behavior stability, and comparison with
  held-out real-human annotations and/or interactions.

A new perceived-association metric should be marked **experimental** until its
annotation protocol, calibration, uncertainty and simple rule/embedding/LLM
baselines are described and evaluated.

## Dataset warning

Amazon ratings/reviews are not step-by-step sessions. Do not pass them off as
logged browsing actions. A synthetic rollout must be clearly marked synthetic.
Any real-world evaluation must use appropriate exposure/action data or a
clearly scoped human-subject study.
