# Makefile for Sphinx documentation of Google MCP Security
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = google-mcp-security # Modified
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile clean setup serve deploy

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Setup dependencies
setup:
	pip install -r requirements.txt

# Serve documentation live with auto-reload
livehtml:
	sphinx-autobuild -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)

# Clean build directory
clean:
	rm -rf $(BUILDDIR)/*

# Build documentation
build: clean
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Serve documentation - alternative to livehtml without auto-reload
serve: build
	python -m http.server --directory $(BUILDDIR)/html 8000

# Deploy to GitHub Pages (if used)
deploy: build
	@echo "To deploy to GitHub Pages, configure your repository settings."
