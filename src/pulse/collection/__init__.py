"""Deterministic evidence collection framework."""

from pulse.collection.planner import CollectionPlan, CollectionTask, TaskKind, plan_collection
from pulse.collection.sources import SOURCE_REGISTRY, SourceCapability

__all__ = [
    "SOURCE_REGISTRY",
    "CollectionPlan",
    "CollectionTask",
    "SourceCapability",
    "TaskKind",
    "plan_collection",
]
