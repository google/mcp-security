"""Utility functions for SecOps MCP."""

import json
import re
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple, Union

_API_VERSION_SUFFIX = re.compile(r"/v1(alpha|beta)?/?$")


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


def parse_json_arg(
    value: Union[None, str, Dict[str, Any], List[Any]],
    name: str,
) -> Union[None, Dict[str, Any], List[Any]]:
    """Accept a JSON object/array passed either natively or as a JSON string.

    MCP clients differ in whether they pass structured arguments as JSON
    values or as JSON-encoded strings. This normalizes both forms.

    Args:
        value: The raw argument value.
        name: Argument name used in error messages.

    Returns:
        The parsed dict/list, or None when value is None or empty string.

    Raises:
        ValueError: If value is a string that is not valid JSON.
    """
    if value is None or value == "":
        return None
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError as e:
            raise ValueError(f"{name} must be valid JSON: {e}") from e
    raise ValueError(f"{name} must be a JSON object/array or JSON string")


def instance_base_url(chronicle: Any, api_version: str = "v1alpha") -> str:
    """Return ``https://<region>-chronicle.googleapis.com/<version>/<instance>``.

    Works across ``secops`` SDK releases: newer releases expose
    ``chronicle.base_url`` as a callable ``BaseUrl`` object that accepts an API
    version, older releases expose a plain string ending in ``/v1alpha``.
    """
    base = chronicle.base_url
    if callable(base):
        base = base(api_version)
    else:
        base = _API_VERSION_SUFFIX.sub(f"/{api_version}", str(base).rstrip("/"))
    return f"{base}/{chronicle.instance_id}"


def chronicle_api_request(
    chronicle: Any,
    method: str,
    path: str,
    *,
    api_version: str = "v1alpha",
    params: Optional[Dict[str, Any]] = None,
    json_body: Optional[Dict[str, Any]] = None,
    timeout: int = 120,
) -> Dict[str, Any]:
    """Issue an authenticated Chronicle REST call relative to the instance.

    Args:
        chronicle: Chronicle client from ``get_chronicle_client``.
        method: HTTP method (``GET``, ``POST``, ``PATCH``, ``DELETE``).
        path: Path after ``.../instances/{instance}``. May start with ``/``
            (sub-resource, e.g. ``/nativeDashboards``) or be a custom verb on
            the instance itself (e.g. ``legacySoarDashboard:legacyGetDashboard``).
            Absolute resource names beginning with ``projects/`` are used as-is
            after the API-version prefix.
        api_version: ``v1alpha`` (default), ``v1beta`` or ``v1``.
        params: Optional query parameters. ``None`` values are dropped.
        json_body: Optional JSON request body.
        timeout: Request timeout in seconds.

    Returns:
        The decoded JSON response (``{}`` for empty bodies).

    Raises:
        RuntimeError: On non-2xx responses, with status and body included.
    """
    base = instance_base_url(chronicle, api_version)
    if path.startswith("projects/"):
        url = f"{base.rsplit('/projects/', 1)[0]}/{path}"
    elif path.startswith("/"):
        url = f"{base}{path}"
    else:
        url = f"{base}/{path}"

    clean_params = (
        {k: v for k, v in params.items() if v is not None} if params else None
    )
    response = chronicle.session.request(
        method,
        url,
        params=clean_params,
        json=json_body,
        timeout=timeout,
    )
    if response.status_code >= 400:
        raise RuntimeError(
            f"Chronicle API {method} {url} failed with status "
            f"{response.status_code}: {response.text}"
        )
    if not response.content:
        return {}
    try:
        return response.json()
    except ValueError:
        return {"raw": response.text}
