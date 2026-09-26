"""Safe collection telemetry, without credentials or response bodies."""

from pydantic import BaseModel, Field


class RequestRecord(BaseModel):
    status_code: int | None = None
    error_type: str | None = None
    remaining: int | None = None
    reset_at: str | None = None
    retry_after: str | None = None


class CollectionStats(BaseModel):
    pages_requested: int = 0
    pages_completed: int = 0
    records_examined: int = 0
    duplicate_records: int = 0
    retry_count: int = 0
    requests: list[RequestRecord] = Field(default_factory=list)
    termination: str | None = None
