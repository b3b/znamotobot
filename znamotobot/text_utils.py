"""Text utils."""
import re


def is_http_url(path: str) -> bool:
    """Check whether a string is HTTP URL."""
    return bool(re.match("^http[s]?://", path))
