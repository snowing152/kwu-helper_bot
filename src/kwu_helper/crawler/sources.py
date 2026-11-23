"""Registry of official university pages the crawler downloads.

The list is fixed in code on purpose: every source is reviewed by a human before the bot
may answer from it, so adding a page is a code change, not a config tweak.
"""

from dataclasses import dataclass
from typing import Literal

Language = Literal["ko", "en"]
SourceKind = Literal["page", "notice_list"]


@dataclass(frozen=True)
class Source:
    """One crawlable source.

    Attributes:
        id: Stable short name, used in the manifest and in citations.
        url: Absolute HTTPS URL.
        kind: "page" is one document; "notice_list" is a board whose posts are documents.
        language: Language of the page content.
        content_selector: CSS selector of the main content area, or None to use <body>.
    """

    id: str
    url: str
    kind: SourceKind
    language: Language
    content_selector: str | None = None


_OIA_BASE = "https://oia.kw.ac.kr/campus/"
_OIA_PAGES = ("visa", "bachelor", "scholarship", "insurance", "dormitory", "work", "FAQ")

_KW_BASE = "https://www.kw.ac.kr/ko/life/"
_KW_BACHELOR_PAGES = ("01", "02", "05", "07", "08", "12", "13")

SOURCES: tuple[Source, ...] = (
    *(
        Source(id=f"oia-{name.lower()}", url=f"{_OIA_BASE}{name}.php", kind="page", language="en")
        for name in _OIA_PAGES
    ),
    *(
        Source(
            id=f"kw-bachelor-info{num}",
            url=f"{_KW_BASE}bachelor_info{num}.jsp",
            kind="page",
            language="ko",
        )
        for num in _KW_BACHELOR_PAGES
    ),
    Source(id="kw-scholarship", url=f"{_KW_BASE}summary.jsp", kind="page", language="ko"),
    Source(
        id="kw-notices-intl",
        url=f"{_KW_BASE}notice.jsp?srCategoryId=10",
        kind="notice_list",
        language="ko",
    ),
)
