"""Local, explicit API and PostgreSQL configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[3]
PUBLISHED_SNAPSHOT_IDS = frozenset(
    {
        UUID("08852d5f-9843-5406-a69b-7039ea2ddaa4"),
        UUID("bd3a02a5-0c2d-5eec-84fd-8e9b93a238a3"),
    }
)


@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    database: str
    user: str
    password: str
    environment: str = "local"

    @classmethod
    def from_environment(cls) -> Settings:
        values = dotenv_values(ROOT / ".env")

        def setting(name: str, default: str = "") -> str:
            return os.environ.get(name) or str(values.get(name) or default)

        result = cls(
            host=setting("PGHOST", "127.0.0.1"),
            port=int(setting("PGPORT", "55432")),
            database=setting("PGDATABASE", "pulse_dev"),
            user=setting("PGUSER", "pulse_local"),
            password=setting("PGPASSWORD"),
            environment=setting("PULSE_API_ENV", "local"),
        )
        if (result.host, result.port, result.user) != ("127.0.0.1", 55432, "pulse_local"):
            raise ValueError("PULSE API is limited to the isolated local PostgreSQL cluster")
        if result.database not in {"pulse_dev", "pulse_test"} or not result.password:
            raise ValueError("PULSE API needs pulse_dev/pulse_test and local credentials")
        return result
