"""Utility functions for SecOps MCP."""

from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple, Union


def parse_iso_datetime(time_input: Union[str, datetime]) -> datetime:
    """Parses an ISO 8601 string or datetime object and returns a UTC timezone-aware datetime.

    Handles trailing 'Z'/'z', explicit timezone offsets (+HH:MM/-HH:MM),
    and naive ISO strings/datetimes (which default to UTC). Always returns a datetime
    normalized to UTC (tzinfo=timezone.utc).

    Args:
        time_input: ISO 8601 formatted date/time string, or an existing datetime object.

    Returns:
        A timezone-aware datetime object with tzinfo=timezone.utc.

    Raises:
        ValueError: If time_input is empty, not a string/datetime, or not a valid ISO 8601 string.
    """
    if isinstance(time_input, datetime):
        if time_input.tzinfo is None:
            time_input = time_input.replace(tzinfo=timezone.utc)
        return time_input.astimezone(timezone.utc)

    if not isinstance(time_input, str) or not time_input.strip():
        raise ValueError(f"Invalid datetime input: {time_input!r}")

    cleaned = time_input.strip()
    if cleaned.endswith(("z", "Z")):
        cleaned = cleaned[:-1] + "+00:00"

    dt = datetime.fromisoformat(cleaned)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def parse_time_range(
    start_time: Optional[Union[str, datetime]],
    end_time: Optional[Union[str, datetime]],
    hours_back: int,
) -> Tuple[datetime, datetime]:
    """Parses ISO strings or defaults to hours_back.

    Args:
        start_time: ISO 8601 start time string or datetime (e.g. 2023-01-01T00:00:00Z).
        end_time: ISO 8601 end time string or datetime.
        hours_back: Fallback hours to look back if start_time is not provided.

    Returns:
        Tuple of (start_dt, end_dt) as timezone-aware datetime objects in UTC.

    Raises:
        ValueError: If the date strings are malformed or start_time is after end_time.
    """
    if end_time:
        end_dt = parse_iso_datetime(end_time)
    else:
        end_dt = datetime.now(timezone.utc)

    if start_time:
        start_dt = parse_iso_datetime(start_time)
    else:
        start_dt = end_dt - timedelta(hours=hours_back)

    if start_dt > end_dt:
        raise ValueError(f"Start time ({start_dt}) cannot be after end time ({end_dt})")

    return start_dt, end_dt
