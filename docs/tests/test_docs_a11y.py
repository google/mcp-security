"""Automated WCAG 2.1 AA and best-practice accessibility suite for Sphinx docs."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator

from axe_playwright_python.sync_playwright import Axe
from bs4 import BeautifulSoup
from playwright.sync_api import Page, sync_playwright
import pytest

SOAR_SAMPLE_LIMIT = 5


def _resolve_html_dir() -> Path:
    """Resolve the built Sphinx HTML directory from HTML_DIR or repo layout."""
    env_dir = os.environ.get("HTML_DIR")
    if env_dir:
        return Path(env_dir).resolve()
    docs_dir = Path(__file__).resolve().parents[1]
    return (docs_dir / "_build" / "html").resolve()


def _collect_all_html_files() -> list[Path]:
    """Return all built HTML files sorted by relative path."""
    html_dir = _resolve_html_dir()
    if not html_dir.is_dir():
        return []
    return sorted(html_dir.rglob("*.html"))


def _collect_axe_target_files() -> list[Path]:
    """Return representative or full HTML file list for Chromium axe-core scans."""
    all_files = _collect_all_html_files()
    if not all_files:
        return []
    if os.environ.get("A11Y_FULL_SCAN") == "1":
        return all_files

    html_dir = _resolve_html_dir()
    core_files: list[Path] = []
    soar_detail_files: list[Path] = []

    for html_file in all_files:
        rel_parts = html_file.relative_to(html_dir).parts
        if rel_parts[0] == "soar_integrations" and html_file.name != "index.html":
            soar_detail_files.append(html_file)
        else:
            core_files.append(html_file)

    return core_files + soar_detail_files[:SOAR_SAMPLE_LIMIT]


def _rel_id(path: Path) -> str:
    """Format a readable pytest parameter ID relative to HTML_DIR."""
    html_dir = _resolve_html_dir()
    try:
        return str(path.relative_to(html_dir))
    except ValueError:
        return str(path)


@pytest.fixture(scope="session")
def themed_pages() -> Iterator[dict[str, Page]]:
    """Provide reusable Chromium pages configured for light and dark schemes."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        contexts = {
            "light": browser.new_context(color_scheme="light"),
            "dark": browser.new_context(color_scheme="dark"),
        }
        pages = {
            scheme: context.new_page() for scheme, context in contexts.items()
        }
        try:
            yield pages
        finally:
            for context in contexts.values():
                context.close()
            browser.close()


def test_html_build_output_present() -> None:
    """Fail explicitly if Sphinx HTML output has not been built."""
    html_dir = _resolve_html_dir()
    html_files = _collect_all_html_files()
    assert html_files, (
        f"No built HTML files found in {html_dir}. "
        "Run 'make -C docs html' before executing accessibility tests."
    )


def test_all_html_pages_static_semantics() -> None:
    """Verify structural WCAG semantics across every generated HTML page."""
    html_dir = _resolve_html_dir()
    html_files = _collect_all_html_files()
    assert html_files, f"No built HTML files found in {html_dir}."

    errors: list[str] = []
    for html_path in html_files:
        rel = html_path.relative_to(html_dir)
        soup = BeautifulSoup(
            html_path.read_text(encoding="utf-8"), "html.parser"
        )

        html_tag = soup.find("html")
        if not html_tag or not str(html_tag.get("lang", "")).strip():
            errors.append(f"{rel}: missing <html lang='...'> attribute")

        title_text = soup.title.get_text(strip=True) if soup.title else ""
        if not title_text:
            errors.append(f"{rel}: missing or empty <title>")

        if not soup.find("h1"):
            errors.append(f"{rel}: missing primary <h1> heading")

        for img in soup.find_all("img"):
            if img.get("alt") is None:
                errors.append(
                    f"{rel}: <img> missing alt attribute ({img.get('src', '')})"
                )

        for heading in soup.find_all(attrs={"role": "heading"}):
            if not heading.get("aria-level"):
                errors.append(
                    f"{rel}: element with role='heading' missing aria-level"
                )

        for pre in soup.find_all("pre"):
            if pre.get("tabindex") is None:
                errors.append(
                    f"{rel}: <pre> block missing tabindex for keyboard scrolling"
                )

        for table_wrapper in soup.select("div.table-wrapper"):
            if table_wrapper.get("tabindex") is None:
                errors.append(
                    f"{rel}: div.table-wrapper missing tabindex for keyboard scrolling"
                )

        for checkbox in soup.select("input.task-list-item-checkbox"):
            if not checkbox.get("aria-label") and not checkbox.get(
                "aria-labelledby"
            ):
                errors.append(
                    f"{rel}: task-list checkbox missing accessible label"
                )

    assert not errors, "Static HTML accessibility errors:\n" + "\n".join(errors)


@pytest.mark.parametrize(
    "html_path",
    _collect_axe_target_files(),
    ids=_rel_id,
)
def test_page_passes_axe_accessibility_checks(
    themed_pages: dict[str, Page],
    html_path: Path,
) -> None:
    """Verify rendered pages pass axe-core WCAG AA and best-practice rules in light and dark themes."""
    axe = Axe()
    page_uri = html_path.resolve().as_uri()
    rel_name = _rel_id(html_path)

    failures: list[str] = []
    for scheme, page in themed_pages.items():
        page.goto(page_uri, wait_until="load")
        page.evaluate(
            "(theme) => { document.body.dataset.theme = theme; }",
            scheme,
        )
        results = axe.run(page)
        violations = results.response.get("violations", [])
        for violation in violations:
            rule_id = violation.get("id", "unknown")
            impact = violation.get("impact", "unknown")
            help_text = violation.get("help", "")
            targets = [
                node.get("target", [])
                for node in violation.get("nodes", [])[:3]
            ]
            failures.append(
                f"[{scheme}] {rel_name} -> {rule_id} ({impact}): {help_text} | targets={targets}"
            )

    assert not failures, "axe-core accessibility violations:\n" + "\n".join(
        failures
    )
