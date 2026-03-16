from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlencode, urlsplit, urlunsplit
from urllib import error, request

from campus_events.models import SourceRecord


@dataclass(slots=True)
class FetchResult:
    ok: bool
    content: str | None
    content_type: str | None
    error: str | None = None


NTU_SPECIAL_EVENT_ENDPOINTS = {
    "ntu_main_events": "https://www.ntu.edu.sg/events/GetEvents/",
    "ntu_cee_events": "https://www.ntu.edu.sg/cee/news-events/events/GetEvents/",
    "ntu_erian_news_events": "https://www.ntu.edu.sg/erian/news-events/events/GetEvents/",
    "ntu_cceb_seminars": "https://www.ntu.edu.sg/cceb/news-and-events/events/GetEvents/",
}

NTU_HTML_LISTING_SOURCES = {
    "ntu_sbs_events",
}


def fetch_source(source: SourceRecord, timeout_seconds: int = 20) -> FetchResult:
    req = _build_request(source)
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


def _build_request(source: SourceRecord) -> request.Request:
    headers = {
        "User-Agent": "CampusEventsDigest/0.1 (+automation-safe dry run)",
    }
    ntu_endpoint = _ntu_event_endpoint_for(source)
    if ntu_endpoint:
        return request.Request(
            ntu_endpoint,
            headers={**headers, "Accept": "application/json"},
        )
    if source.id == "ntu_scelse_all_events":
        payload = urlencode(
            {
                "action": "get_all_posts_by_page",
                "number": "_1",
                "page_id": "250728",
                "post_type": "event",
            }
        ).encode("utf-8")
        return request.Request(
            "https://scelse.sg/wp-admin/admin-ajax.php",
            data=payload,
            headers={
                **headers,
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Origin": "https://scelse.sg",
                "Referer": source.url,
            },
            method="POST",
        )
    return request.Request(source.url, headers=headers)


def _ntu_event_endpoint_for(source: SourceRecord) -> str | None:
    if source.id in NTU_HTML_LISTING_SOURCES:
        return None
    if source.id in NTU_SPECIAL_EVENT_ENDPOINTS:
        return NTU_SPECIAL_EVENT_ENDPOINTS[source.id]
    if source.parser_family in {"ntu_event_portal", "ntu_event_detail_listing"}:
        parsed = urlsplit(source.url)
        clean_path = parsed.path.rstrip("/") + "/GetEvents/"
        return urlunsplit((parsed.scheme, parsed.netloc, clean_path, "", ""))
    return None
