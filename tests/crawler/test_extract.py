import pytest

from kwu_helper.crawler.extract import (
    MIN_TEXT_CHARS,
    EmptyContentError,
    decode_html,
    extract_page,
)

BASE = "https://www.kw.ac.kr/ko/life/x.jsp"
# Long enough to pass MIN_TEXT_CHARS on its own.
FILLER = "학사 규정에 대한 안내 문장입니다. " * 20


def page(body: str, head: str = "") -> str:
    return f"<html><head>{head}</head><body>{body}</body></html>"


def test_filler_is_long_enough() -> None:
    assert len(FILLER) >= MIN_TEXT_CHARS


def test_decode_euc_kr_without_charset_header() -> None:
    body = '<html><head><meta charset="euc-kr"></head><body>졸업요건</body></html>'.encode("euc-kr")
    assert "졸업요건" in decode_html(body, "text/html")


def test_decode_utf8_with_header() -> None:
    body = page("학칙").encode("utf-8")
    assert "학칙" in decode_html(body, "text/html; charset=utf-8")


def test_decode_euc_kr_body_with_wrong_utf8_header() -> None:
    body = page("휴학 신청").encode("euc-kr")
    assert "휴학 신청" in decode_html(body, "text/html; charset=utf-8")


def test_extract_removes_nav_script_and_footer() -> None:
    html = page(f"<nav>MENU</nav><script>x()</script><main>{FILLER}</main><footer>FOOT</footer>")
    text = extract_page(html, BASE, None).text
    assert "학사 규정" in text
    for noise in ("MENU", "x()", "FOOT"):
        assert noise not in text


def test_extract_keeps_table_rows_with_separator() -> None:
    table = "<table><tr><th>구분</th><th>학점</th></tr><tr><td>전공</td><td>60</td></tr></table>"
    lines = extract_page(page(table + FILLER), BASE, None).text.splitlines()
    assert "구분 | 학점" in lines
    assert "전공 | 60" in lines


def test_extract_uses_selector_when_given() -> None:
    html = page(f"<div id='side'>SIDEBAR</div><div id='content'>{FILLER}</div>")
    text = extract_page(html, BASE, "#content").text
    assert "SIDEBAR" not in text
    assert "학사 규정" in text


def test_extract_raises_when_selector_matches_nothing() -> None:
    with pytest.raises(EmptyContentError):
        extract_page(page(FILLER), BASE, "#missing")


def test_extract_collects_absolute_attachment_urls() -> None:
    links = '<a href="/files/rule.PDF">r</a><a href="a.hwp">a</a><a href="page.jsp">p</a>'
    result = extract_page(page(links + FILLER), BASE, None)
    assert result.attachment_urls == (
        "https://www.kw.ac.kr/files/rule.PDF",
        "https://www.kw.ac.kr/ko/life/a.hwp",
    )


def test_extract_title_prefers_title_tag_then_heading() -> None:
    assert extract_page(page(FILLER, "<title> 졸업 </title>"), BASE, None).title == "졸업"
    assert extract_page(page(f"<h1>장학금</h1>{FILLER}"), BASE, None).title == "장학금"


def test_extract_collapses_whitespace_and_drops_empty_lines() -> None:
    text = extract_page(page(f"<p>a    b</p><p>   </p><p>{FILLER}</p>"), BASE, None).text
    assert text.splitlines()[0] == "a b"
    assert "" not in text.splitlines()


def test_extract_raises_on_near_empty_content() -> None:
    with pytest.raises(EmptyContentError):
        extract_page(page("<div id='app'>Loading...</div>"), "https://x", None)
