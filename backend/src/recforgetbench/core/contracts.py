"""Stable cross-module contracts; change only through an approved contract PR."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class RunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class DatasetRef(BaseModel):
    dataset_id: str = Field(min_length=1)
    version: str = Field(min_length=1)
    metadata_uri: str | None = None


class SplitRef(BaseModel):
    split_id: str = Field(min_length=1)
    dataset: DatasetRef
    seed: int = Field(ge=0)
    train_manifest_uri: str
    validation_manifest_uri: str
    test_manifest_uri: str


class ForgetRequest(BaseModel):
    request_id: str = Field(min_length=1)
    split_id: str = Field(min_length=1)
    strategy: str = "interaction"
    forget_manifest_uri: str = Field(min_length=1)
    retain_manifest_uri: str = Field(min_length=1)
    seed: int = Field(ge=0)


class ModelArtifact(BaseModel):
    model_id: str = Field(min_length=1)
    dataset_id: str = Field(min_length=1)
    split_id: str = Field(min_length=1)
    model_name: str = Field(min_length=1)
    checkpoint_uri: str = Field(min_length=1)
    id_mapping_uri: str = Field(min_length=1)
    config: dict[str, Any] = Field(default_factory=dict)
    parent_model_id: str | None = None
    forget_request_id: str | None = None


class RunRecord(BaseModel):
    run_id: str = Field(min_length=1)
    task_type: str = Field(min_length=1)
    status: RunStatus = RunStatus.PENDING
    config: dict[str, Any] = Field(default_factory=dict)
    artifacts: list[str] = Field(default_factory=list)
    error_message: str | None = None
