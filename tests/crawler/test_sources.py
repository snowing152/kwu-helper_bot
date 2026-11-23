from urllib.parse import urlparse

from kwu_helper.crawler.sources import SOURCES


def test_source_ids_are_unique() -> None:
    ids = [s.id for s in SOURCES]
    assert len(ids) == len(set(ids))


def test_all_sources_use_https_on_kw_domains() -> None:
    for s in SOURCES:
        assert s.url.startswith("https://")
        assert urlparse(s.url).hostname in {"oia.kw.ac.kr", "www.kw.ac.kr"}


def test_exactly_one_notice_list() -> None:
    assert [s.kind for s in SOURCES].count("notice_list") == 1


def test_registry_has_planned_page_counts() -> None:
    by_language = [s.language for s in SOURCES if s.kind == "page"]
    assert by_language.count("en") == 7
    assert by_language.count("ko") == 8
