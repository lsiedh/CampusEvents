from __future__ import annotations

from dataclasses import dataclass
from urllib import error, request

from campus_events.models import SourceRecord


@dataclass(slots=True)
class FetchResult:
    ok: bool
    content: str | None
    content_type: str | None
    error: str | None = None


def fetch_source(source: SourceRecord, timeout_seconds: int = 20) -> FetchResult:
    req = request.Request(
        source.url,
        headers={
            "User-Agent": "CampusEventsDigest/0.1 (+automation-safe dry run)",
        },
    )
    try:
        with request.urlopen(req, timeout=timeout_seconds) as response:
            body = response.read().decode("utf-8", errors="replace")
            content_type = response.headers.get_content_type()
            return FetchResult(ok=True, content=body, content_type=content_type)
    except error.HTTPError as exc:
        return FetchResult(ok=False, content=None, content_type=None, error=f"HTTP {exc.code}")
    except error.URLError as exc:
        return FetchResult(
            ok=False,
            content=None,
            content_type=None,
            error=str(exc.reason),
        )
    except TimeoutError:
        return FetchResult(ok=False, content=None, content_type=None, error="timeout")
    except Exception as exc:  # pragma: no cover - defensive logging path
        return FetchResult(ok=False, content=None, content_type=None, error=str(exc))

