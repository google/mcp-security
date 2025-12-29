"""Utility functions for SecOps MCP."""

from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

def parse_time_range(
    start_time: Optional[str], 
    end_time: Optional[str], 
    hours_back: int
) -> Tuple[datetime, datetime]:
    """Parses ISO strings or defaults to hours_back.
    
    Args:
        start_time: ISO 8601 start time string (e.g. 2023-01-01T00:00:00Z).
        end_time: ISO 8601 end time string.
        hours_back: Fallback hours to look back if start_time is not provided.
        
    Returns:
        Tuple of (start_dt, end_dt) as timezone-aware datetime objects.
        
    Raises:
        ValueError: If the date strings are malformed or start_time is after end_time.
    """
    # Parse end_time if provided, otherwise default to now
    if end_time:
        end_dt = datetime.fromisoformat(end_time)
        if end_dt.tzinfo is None:
            end_dt = end_dt.replace(tzinfo=timezone.utc)
    else:
        end_dt = datetime.now(timezone.utc)

    # Parse start_time if provided
    if start_time:
        start_dt = datetime.fromisoformat(start_time)
        if start_dt.tzinfo is None:
            start_dt = start_dt.replace(tzinfo=timezone.utc)
    else:
        # Fallback to hours_back from end_dt
        start_dt = end_dt - timedelta(hours=hours_back)
            
    if start_dt > end_dt:
        raise ValueError(f"Start time ({start_dt}) cannot be after end time ({end_dt})")
        
    return start_dt, end_dt
