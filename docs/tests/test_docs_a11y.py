import os
from playwright.sync_api import sync_playwright
import pytest

def get_html_files():
    html_dir = os.environ.get("HTML_DIR", "docs/_build/html")
    if not os.path.exists(html_dir):
        return []
    files = []
    for root, _, filenames in os.walk(html_dir):
        for f in filenames:
            if f.endswith(".html"):
                files.append(os.path.join(root, f))
    return files

@pytest.mark.parametrize("html_path", get_html_files() or ["SKIP"])
def sub_test_page_a11y(html_path):
    if html_path == "SKIP":
        pytest.skip("No HTML files built yet")
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Test both light and dark color schemes
        for scheme in ["light", "dark"]:
            context = browser.new_context(color_scheme=scheme)
            page = context.new_page()
            
            abs_path = os.path.abspath(html_path)
            page.goto(f"file://{abs_path}")
            
            # Inject axe-core from CDN or local if available
            page.add_script_tag(url="https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.8.3/axe.min.js")
            
            # Run axe evaluation
            results = page.evaluate("async () => await axe.run()")
            violations = results.get("violations", [])
            
            assert len(violations) == 0, f"Accessibility violations found in {html_path} ({scheme} mode): {violations}"
            context.close()
        browser.close()
