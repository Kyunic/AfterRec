"""Boundary between simulated users, recommendation models, and environment."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, model_validator


class RecommendedItem(BaseModel):
    item_id: str = Field(min_length=1)
    score: float
    rank: int = Field(ge=1)
    title: str | None = None
    category: str | None = None


class SessionState(BaseModel):
    """Feedback state, never the recommender model's trainable parameters."""

    clicked_items: list[str] = Field(default_factory=list)
    disliked_items: list[str] = Field(default_factory=list)


class ActionType(str, Enum):
    CLICK = "click"
    DISLIKE = "dislike"
    SKIP = "skip"
    EXIT = "exit"


class AgentAction(BaseModel):
    type: ActionType
    item_id: str | None = None

    @model_validator(mode="after")
    def validate_target(self) -> "AgentAction":
        item_targeted = self.type in (ActionType.CLICK, ActionType.DISLIKE)
        if item_targeted and not self.item_id:
            raise ValueError("click/dislike requires an item_id")
        if not item_targeted and self.item_id is not None:
            raise ValueError("skip/exit must not specify an item_id")
        return self


class AgentObservation(BaseModel):
    user_id: str
    step: int = Field(ge=1)
    persona: dict[str, Any] = Field(default_factory=dict)
    forgetting_intent: str
    items: list[RecommendedItem]
    recent_actions: list[AgentAction] = Field(default_factory=list)


class InteractionEvent(BaseModel):
    step: int
    displayed_items: list[RecommendedItem]
    action: AgentAction


class SimulationTrace(BaseModel):
    user_id: str
    model_id: str
    events: list[InteractionEvent]
    terminated: bool
    synthetic: bool = True
