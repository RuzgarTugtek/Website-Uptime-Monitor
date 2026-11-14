"""SQLite storage for HTTP monitoring results."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .monitor import CheckResult


def save_result(database_path: Path, result: CheckResult) -> None:
    """Write a check result to a local SQLite file with parameterized SQL."""
    with sqlite3.connect(database_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS uptime_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                checked_at TEXT NOT NULL,
                url TEXT NOT NULL,
                status_code INTEGER,
                latency_ms REAL NOT NULL,
                is_up INTEGER NOT NULL,
                error TEXT
            )
            """
        )
        connection.execute(
            """
            INSERT INTO uptime_checks
                (checked_at, url, status_code, latency_ms, is_up, error)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                result.checked_at,
                result.url,
                result.status_code,
                result.latency_ms,
                int(result.is_up),
                result.error,
            ),
        )


def read_summary(database_path: Path) -> list[dict[str, object]]:
    """Summarize stored checks per URL without making new HTTP requests."""
    if not database_path.is_file():
        raise FileNotFoundError(f"No monitoring database found: {database_path}")

    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT
                history.url,
                COUNT(*) AS total_checks,
                SUM(history.is_up) AS up_checks,
                ROUND(100.0 * SUM(history.is_up) / COUNT(*), 2) AS uptime_percent,
                ROUND(
                    AVG(CASE WHEN history.is_up = 1 THEN history.latency_ms END), 2
                ) AS average_up_latency_ms,
                (
                    SELECT recent.is_up
                    FROM uptime_checks AS recent
                    WHERE recent.url = history.url
                    ORDER BY recent.id DESC
                    LIMIT 1
                ) AS last_is_up
            FROM uptime_checks AS history
            GROUP BY history.url
            ORDER BY history.url
            """
        ).fetchall()

    return [
        {
            "url": row["url"],
            "total_checks": row["total_checks"],
            "up_checks": row["up_checks"],
            "uptime_percent": row["uptime_percent"],
            "average_up_latency_ms": row["average_up_latency_ms"],
            "last_status": "UP" if row["last_is_up"] else "DOWN",
        }
        for row in rows
    ]
