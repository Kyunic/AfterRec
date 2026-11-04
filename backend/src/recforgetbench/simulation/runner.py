"""Minimal deterministic simulation loop with strict action validation.

Only a runtime scaffold, not a validated human-behavior simulator.
"""

from collections.abc import Callable, Sequence
from typing import Protocol

from recforgetbench.simulation.contracts import (
    ActionType,
    AgentAction,
    AgentObservation,
    InteractionEvent,
    RecommendedItem,
    SessionState,
    SimulationTrace,
)


class AgentPolicy(Protocol):
    def act(self, observation: AgentObservation) -> AgentAction: ...


class FrozenRecommendationProvider(Protocol):
    def recommend(
        self, user_id: str, top_k: int, state: SessionState
    ) -> Sequence[RecommendedItem]: ...


def run_episode(
    *,
    user_id: str,
    model_id: str,
    persona: dict,
    forgetting_intent: str,
    agent: AgentPolicy,
    recommender: FrozenRecommendationProvider,
    max_steps: int = 5,
    top_k: int = 10,
    on_step: Callable[[InteractionEvent], None] | None = None,
) -> SimulationTrace:
    """Run a bounded episode; the recommender never receives the forgetting intent.

    Recommender is supplied once, must be frozen by the caller. Each experiment
    arm must start with fresh agent and session state to avoid cross-arm leakage.
    """
    if not (1 <= max_steps <= 100) or top_k <= 0:
        raise ValueError("Invalid episode budget")
    state = SessionState()
    events: list[InteractionEvent] = []
    terminated = False

    for step in range(1, max_steps + 1):
        items = list(recommender.recommend(user_id, top_k, state.model_copy(deep=True)))
        item_ids = [item.item_id for item in items]
        if len(item_ids) != len(set(item_ids)):
            raise ValueError("Recommender returned duplicate item IDs")
        observation = AgentObservation(
            user_id=user_id,
            step=step,
            persona=persona.copy(),
            forgetting_intent=forgetting_intent,
            items=items,
            recent_actions=[event.action for event in events],
        )
        action = agent.act(observation)
        if action.item_id is not None and action.item_id not in item_ids:
            raise ValueError("Agent attempted to act on an item not currently displayed")
        event = InteractionEvent(step=step, displayed_items=items, action=action)
        events.append(event)
        if on_step:
            on_step(event)
        if action.type == ActionType.CLICK:
            state.clicked_items.append(action.item_id)  # type: ignore[arg-type]
        elif action.type == ActionType.DISLIKE:
            state.disliked_items.append(action.item_id)  # type: ignore[arg-type]
        elif action.type == ActionType.EXIT:
            terminated = True
            break

    return SimulationTrace(user_id=user_id, model_id=model_id, events=events, terminated=terminated)
