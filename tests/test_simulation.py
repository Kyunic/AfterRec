import pytest

from recforgetbench.simulation.contracts import ActionType, AgentAction, RecommendedItem
from recforgetbench.simulation.runner import run_episode


class ToyRecommender:
    def __init__(self):
        self.feedback_states = []

    def recommend(self, user_id, top_k, state):
        self.feedback_states.append(state.model_copy(deep=True))
        # The next recommendation changes only because of the independent state.
        if "p1" in state.disliked_items:
            return [RecommendedItem(item_id="p2", score=0.8, rank=1)]
        return [RecommendedItem(item_id="p1", score=0.9, rank=1)]


class DislikeThenExitAgent:
    def act(self, observation):
        if observation.step == 1:
            return AgentAction(type=ActionType.DISLIKE, item_id="p1")
        return AgentAction(type=ActionType.EXIT)


class InvalidTargetAgent:
    def act(self, observation):
        return AgentAction(type=ActionType.CLICK, item_id="not-visible")


def test_episode_is_bounded_and_responds_to_dislike():
    recommender = ToyRecommender()
    result = run_episode(
        user_id="u1",
        model_id="model-1",
        persona={"preferences": ["sports"]},
        forgetting_intent="Forget basketball interactions",
        agent=DislikeThenExitAgent(),
        recommender=recommender,
    )
    assert result.synthetic is True
    assert result.terminated is True
    assert len(result.events) == 2
    assert result.events[0].displayed_items[0].item_id == "p1"
    assert result.events[1].displayed_items[0].item_id == "p2"
    assert recommender.feedback_states[1].disliked_items == ["p1"]


def test_agent_cannot_act_on_unseen_item():
    with pytest.raises(ValueError, match="not currently displayed"):
        run_episode(
            user_id="u1",
            model_id="m",
            persona={},
            forgetting_intent="forget",
            agent=InvalidTargetAgent(),
            recommender=ToyRecommender(),
        )


def test_action_schema_rejects_invalid_target():
    with pytest.raises(ValueError, match="requires an item_id"):
        AgentAction(type="click")


def test_action_schema_rejects_extraneous_target():
    with pytest.raises(ValueError, match="must not specify"):
        AgentAction(type="exit", item_id="p1")
