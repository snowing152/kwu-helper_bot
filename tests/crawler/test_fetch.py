import time
from collections.abc import Callable

import httpx
import pytest

from kwu_helper.crawler.fetch import FetchError, FetchResult, RateLimiter, fetch, make_client

URL = "https://www.kw.ac.kr/x"
Handler = Callable[[httpx.Request], httpx.Response]


def counting(responses: list[httpx.Response | Exception]) -> tuple[Handler, list[httpx.Request]]:
    """Build a MockTransport handler that replays `responses` in order and records requests."""
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        item = responses[min(len(seen), len(responses)) - 1]
        if isinstance(item, Exception):
            raise item
        return item

    return handler, seen


async def run_fetch(handler: Handler) -> FetchResult:
    async with make_client(httpx.MockTransport(handler)) as client:
        return await fetch(client, RateLimiter(0), URL, backoff_s=0)


async def test_fetch_returns_body_and_sets_user_agent() -> None:
    handler, seen = counting(
        [httpx.Response(200, content=b"<html>ok</html>", headers={"content-type": "text/html"})]
    )
    async with make_client(httpx.MockTransport(handler)) as client:
        result = await fetch(client, RateLimiter(0), URL, backoff_s=0)
    assert result.body == b"<html>ok</html>"
    assert result.status_code == 200
    assert result.content_type == "text/html"
    assert result.fetched_at.tzinfo is not None
    assert seen[0].headers["user-agent"] == "kwu-helper-crawler/0.1 (student project)"


async def test_fetch_retries_on_503_then_succeeds() -> None:
    handler, seen = counting(
        [httpx.Response(503), httpx.Response(503), httpx.Response(200, content=b"ok")]
    )
    await run_fetch(handler)
    assert len(seen) == 3


async def test_fetch_raises_after_max_attempts_on_timeout() -> None:
    handler, seen = counting([httpx.ConnectTimeout("slow")])
    with pytest.raises(FetchError) as excinfo:
        await run_fetch(handler)
    assert len(seen) == 3
    assert excinfo.value.url == URL


async def test_fetch_does_not_retry_404() -> None:
    handler, seen = counting([httpx.Response(404)])
    with pytest.raises(FetchError) as excinfo:
        await run_fetch(handler)
    assert len(seen) == 1
    assert "404" in excinfo.value.reason


async def test_rate_limiter_spaces_calls() -> None:
    limiter = RateLimiter(0.2)
    start = time.monotonic()
    for _ in range(3):
        await limiter.wait()
    assert time.monotonic() - start >= 0.4
