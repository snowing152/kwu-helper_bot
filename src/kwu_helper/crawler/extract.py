"""Turn raw HTML bytes into clean text that later stages can chunk and embed.

Two problems specific to Korean university sites drive this module:
- Older pages are EUC-KR, and some send a wrong or missing charset header.
- Key facts (credits per category) live in tables, so table structure must survive
  as readable rows instead of a soup of cell text.
"""

import logging
import re
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup, Tag

logger = logging.getLogger(__name__)

MIN_TEXT_CHARS = 200

_NOISE_TAGS = ("script", "style", "nav", "header", "footer", "noscript")
_ATTACHMENT_EXTENSIONS = (".pdf", ".hwp", ".hwpx", ".doc", ".docx", ".xls", ".xlsx")
_META_CHARSET = re.compile(rb"""<meta[^>]+charset\s*=\s*["']?([\w-]+)""", re.IGNORECASE)
_HEADER_CHARSET = re.compile(r"charset\s*=\s*[\"']?([\w-]+)", re.IGNORECASE)
# CP949 is Microsoft's superset of EUC-KR; it decodes characters EUC-KR rejects.
_CHARSET_ALIASES = {"euc-kr": "cp949", "euckr": "cp949", "ks_c_5601-1987": "cp949"}


@dataclass(frozen=True)
class ExtractedPage:
    """Clean content of one HTML page.

    Attributes:
        title: Page title, or "" if none was found.
        text: Plain text, one logical line per line; table rows as "cell | cell".
        attachment_urls: Absolute URLs of linked documents (PDF, HWP, Office files).
    """

    title: str
    text: str
    attachment_urls: tuple[str, ...]


class EmptyContentError(Exception):
    """The page has no usable content (JS-rendered page, wrong selector, error page)."""


def _normalize_charset(name: str) -> str:
    lowered = name.lower()
    return _CHARSET_ALIASES.get(lowered, lowered)


def decode_html(body: bytes, content_type: str | None) -> str:
    """Decode HTML bytes, trusting declared charsets only if they actually decode.

    Tries in order: the Content-Type charset, the <meta> charset, UTF-8, CP949.
    """
    candidates: list[str] = []
    if content_type and (match := _HEADER_CHARSET.search(content_type)):
        candidates.append(match.group(1))
    if match_meta := _META_CHARSET.search(body[:4096]):
        candidates.append(match_meta.group(1).decode("ascii"))
    candidates += ["utf-8", "cp949"]

    for name in dict.fromkeys(_normalize_charset(c) for c in candidates):
        try:
            return body.decode(name)
        except (UnicodeDecodeError, LookupError):
            continue
    logger.warning("no charset decoded cleanly; using UTF-8 with replacement characters")
    return body.decode("utf-8", errors="replace")


def _title(soup: BeautifulSoup) -> str:
    for tag_name in ("title", "h1", "h2"):
        tag = soup.find(tag_name)
        if tag is not None and (text := tag.get_text(" ", strip=True)):
            return text
    return ""


def _attachment_urls(region: Tag, base_url: str) -> tuple[str, ...]:
    urls: list[str] = []
    for link in region.find_all("a", href=True):
        href = str(link["href"])
        if urlparse(href).path.lower().endswith(_ATTACHMENT_EXTENSIONS):
            urls.append(urljoin(base_url, href))
    return tuple(dict.fromkeys(urls))


def _flatten_tables(region: Tag) -> None:
    """Replace each table with its rows as text lines, so rows stay together."""
    for table in region.find_all("table"):
        rows = []
        for row in table.find_all("tr"):
            cells = [c.get_text(" ", strip=True) for c in row.find_all(["th", "td"])]
            if any(cells):
                rows.append(" | ".join(cells))
        table.replace_with("\n" + "\n".join(rows) + "\n")


def _clean_lines(raw: str) -> str:
    lines = (" ".join(line.split()) for line in raw.splitlines())
    return "\n".join(line for line in lines if line)


def extract_page(html: str, base_url: str, content_selector: str | None) -> ExtractedPage:
    """Extract title, clean text and attachment links from an HTML page.

    Args:
        html: Decoded HTML (see `decode_html`).
        base_url: URL of the page, used to make relative links absolute.
        content_selector: CSS selector of the main content area; None uses <body>.

    Raises:
        EmptyContentError: if the selector matches nothing or the text is shorter
            than MIN_TEXT_CHARS.
    """
    soup = BeautifulSoup(html, "html.parser")
    title = _title(soup)
    for tag in soup.find_all(_NOISE_TAGS):
        tag.decompose()

    region = soup.select_one(content_selector) if content_selector else (soup.body or soup)
    if region is None:
        raise EmptyContentError(f"selector {content_selector!r} matched nothing at {base_url}")

    attachments = _attachment_urls(region, base_url)
    _flatten_tables(region)
    text = _clean_lines(region.get_text("\n"))
    if len(text) < MIN_TEXT_CHARS:
        raise EmptyContentError(f"only {len(text)} characters of text at {base_url}")
    return ExtractedPage(title=title, text=text, attachment_urls=attachments)
