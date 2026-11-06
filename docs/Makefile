# Makefile for Sphinx documentation of Google MCP Security
#

SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = google-mcp-security
SOURCEDIR     = .
BUILDDIR      = _build

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile clean setup serve deploy lint-docs test-a11y

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

setup:
	pip install -r requirements.txt

livehtml:
	sphinx-autobuild -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

clean:
	rm -rf $(BUILDDIR)/*

build: clean
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

serve: build
	python -m http.server --directory $(BUILDDIR)/html 8000

deploy: build
	@echo "To deploy to GitHub Pages, configure your repository settings."

lint-docs:
	npx -y markdownlint-cli2 "docs/**/*.md"

test-a11y: build
	HTML_DIR="$(BUILDDIR)/html" pytest tests/test_docs_a11y.py
