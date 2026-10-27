#!/usr/bin/env python3
"""
Import validation script for CI/CD pipeline.

This script tests all Python modules across server directories to catch
import errors, invalid typing imports, and missing dependencies that could
break production deployments.
"""

import importlib.util
import os
import sys

SKIP_FILES = {"setup.py", "example.py", "conftest.py", "__init__.py"}
SKIP_DIRS = {"tests", "__pycache__", ".venv", "build", "dist", "egg-info"}

SERVER_CONFIGS = [
    {"dir": "server/gti", "pkg_root": "server/gti"},
    {"dir": "server/scc", "pkg_root": "server/scc"},
    {"dir": "server/secops", "pkg_root": "server/secops"},
    {"dir": "server/secops-soar", "pkg_root": "server/secops-soar"},
]


def file_to_module_name(filepath: str, pkg_root: str) -> str:
    """Converts a file path to its Python module import name."""
    rel = os.path.relpath(filepath, pkg_root)
    no_ext = os.path.splitext(rel)[0]
    return no_ext.replace(os.path.sep, ".")


def find_server_modules():
    """Finds all importable Python modules across server directories."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    modules = []

    for cfg in SERVER_CONFIGS:
        full_pkg_root = os.path.join(repo_root, cfg["pkg_root"])
        if not os.path.exists(full_pkg_root):
            continue

        if full_pkg_root not in sys.path:
            sys.path.insert(0, full_pkg_root)

        full_search_dir = os.path.join(repo_root, cfg["dir"])
        for root, dirs, files in os.walk(full_search_dir):
            dirs[:] = [
                d
                for d in dirs
                if d not in SKIP_DIRS and not d.endswith(".egg-info")
            ]

            for f in sorted(files):
                if (
                    not f.endswith(".py")
                    or f in SKIP_FILES
                    or f.startswith("test_")
                    or f.endswith("_test.py")
                ):
                    continue

                full_path = os.path.join(root, f)
                mod_name = file_to_module_name(full_path, full_pkg_root)
                modules.append((mod_name, full_path))

    return modules


def run_import_checks():
    """Attempts to import all discovered modules and returns a list of failed files."""
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    for cfg in SERVER_CONFIGS:
        full_pkg_root = os.path.join(repo_root, cfg["pkg_root"])
        if os.path.exists(full_pkg_root) and full_pkg_root not in sys.path:
            sys.path.insert(0, full_pkg_root)

    modules = find_server_modules()
    failed = []

    print(f"Testing {len(modules)} Python modules across server packages...")
    for mod_name, full_path in modules:
        try:
            spec = importlib.util.spec_from_file_location(mod_name, full_path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Could not load spec for {full_path}")
            mod = importlib.util.module_from_spec(spec)
            sys.modules[mod_name] = mod
            spec.loader.exec_module(mod)
        except Exception as e:  # noqa: BLE001
            print(f"✗ {full_path} ({mod_name}): {e}")
            failed.append((full_path, mod_name, str(e)))

    return failed


def main():
    failed = run_import_checks()
    if failed:
        print(f"\n{len(failed)} module(s) failed import tests:")
        for path, mod, err in failed:
            print(f"  - {mod} ({path}): {err}")
        return 1
    else:
        print("✓ All Python modules import successfully")
        return 0


if __name__ == "__main__":
    sys.exit(main())