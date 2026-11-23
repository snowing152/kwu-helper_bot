"""Polite HTTP fetching: one shared client, a global rate limit, and bounded retries."""

import asyncio
import logging
import time
from dataclasses import dataclass
from datetime import UTC, datetime

import httpx

logger = logging.getLogger(__name__)

USER_AGENT = "kwu-helper-crawler/0.1 (student project)"
TIMEOUT_S = 20.0


@dataclass(frozen=True)
class FetchResult:
    """A successful (2xx) response.

    Attributes:
        url: The URL that was requested.
        status_code: HTTP status code of the final response.
        body: Raw response bytes; decoding is the extractor's job (pages may be EUC-KR).
        content_type: The Content-Type header, if any.
        fetched_at: UTC time the response arrived.
    """

    url: str
    status_code: int
    body: bytes
    content_type: str | None
    fetched_at: datetime


class FetchError(Exception):
    """A URL could not be fetched after all allowed attempts."""

    def __init__(self, url: str, reason: str) -> None:
        super().__init__(f"{url}: {reason}")
        self.url = url
        self.reason = reason


class RateLimiter:
    """Enforce a minimum interval between requests, shared by all callers.

    The lock makes concurrent callers queue up, so the interval holds even if the
    crawler later fetches in parallel.
    """

    def __init__(self, min_interval_s: float = 1.0) -> None:
        self._min_interval_s = min_interval_s
        self._last: float | None = None
        self._lock = asyncio.Lock()

    async def wait(self) -> None:
        """Sleep until at least `min_interval_s` has passed since the previous call."""
        async with self._lock:
            now = time.monotonic()
            if self._last is not None:
                delay = self._last + self._min_interval_s - now
                if delay > 0:
                    await asyncio.sleep(delay)
            self._last = time.monotonic()


def make_client(transport: httpx.AsyncBaseTransport | None = None) -> httpx.AsyncClient:
    """Create the crawler's HTTP client. Pass `transport` to replace the network in tests."""
    return httpx.AsyncClient(
        headers={"User-Agent": USER_AGENT},
        timeout=TIMEOUT_S,
        follow_redirects=True,
        transport=transport,
    )


def _is_retryable_status(status_code: int) -> bool:
    # 5xx means the server failed and may recover; 4xx means our request is wrong
    # (or the page is gone), so repeating it only adds load.
    return status_code >= 500


async def fetch(
    client: httpx.AsyncClient,
    limiter: RateLimiter,
    url: str,
    *,
    max_attempts: int = 3,
    backoff_s: float = 0.5,
) -> FetchResult:
    """Fetch `url`, retrying timeouts, connection errors and 5xx responses.

    Waits with exponential backoff between attempts: `backoff_s` before the second,
    `2 * backoff_s` before the third, and so on.

    Raises:
        FetchError: on a non-retryable status, or when all attempts fail.
    """
    reason = "no attempt made"
    for attempt in range(max_attempts):
        if attempt > 0 and backoff_s > 0:
            await asyncio.sleep(backoff_s * 2 ** (attempt - 1))
        await limiter.wait()
        try:
            response = await client.get(url)
        except httpx.TransportError as exc:
            reason = f"{type(exc).__name__}: {exc}"
            logger.warning(
                "attempt %d/%d failed for %s: %s", attempt + 1, max_attempts, url, reason
            )
            continue

        if response.is_success:
            return FetchResult(
                url=url,
                status_code=response.status_code,
                body=response.content,
                content_type=response.headers.get("content-type"),
                fetched_at=datetime.now(UTC),
            )
        reason = f"HTTP {response.status_code}"
        if not _is_retryable_status(response.status_code):
            raise FetchError(url, reason)
        logger.warning("attempt %d/%d failed for %s: %s", attempt + 1, max_attempts, url, reason)

    raise FetchError(url, f"gave up after {max_attempts} attempts, last error: {reason}")
