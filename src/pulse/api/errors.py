"""Small stable client-visible error vocabulary."""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel


class ErrorBody(BaseModel):
    code: str
    message: str


@dataclass
class ApiError(Exception):
    code: str
    message: str
    status: int


def missing(code: str = "NOT_FOUND_IN_SELECTED_COHORT") -> ApiError:
    return ApiError(code, "Resource is not in the selected published investigation", 404)
