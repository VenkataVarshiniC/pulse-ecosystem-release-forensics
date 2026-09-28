"""Drop only the four dbt-owned local schemas before a clean M2.3 rebuild."""

from __future__ import annotations

import argparse

from psycopg import sql

from pulse.phase2_postgres.loader import connect

DBT_SCHEMAS = ("dbt_staging", "dbt_intermediate", "dbt_test__audit", "dbt_scratch")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dbt-only", action="store_true", required=True)
    parser.parse_args()
    with connect("pulse_dev") as conn, conn.transaction():
        database = conn.execute("SELECT current_database()").fetchone()[0]
        if database != "pulse_dev":
            raise ValueError("Refusing to reset a non-development database")
        for name in DBT_SCHEMAS:
            conn.execute(sql.SQL("DROP SCHEMA IF EXISTS {} CASCADE").format(sql.Identifier(name)))
    print("Dropped only dbt-owned schemas: " + ", ".join(DBT_SCHEMAS))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
