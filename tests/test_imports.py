"""Unit test to validate that all server package modules are importable."""

import os
import sys

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from tests.check_imports import run_import_checks


def test_all_server_modules_importable():
    failed = run_import_checks()
    assert not failed, f"{len(failed)} module(s) failed import: {failed}"
