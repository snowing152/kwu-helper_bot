import kwu_helper


def test_package_has_version() -> None:
    assert kwu_helper.__version__ == "0.1.0"
