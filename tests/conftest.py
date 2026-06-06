import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run-perft",
        action="store_true",
        default=False,
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-perft"):
        return

    skip_perft = pytest.mark.skip()
    for item in items:
        if "perft" in item.keywords:
            item.add_marker(skip_perft)
