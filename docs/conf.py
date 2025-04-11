#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import os
import sys
from subprocess import PIPE, Popen

# Add parent directory to path for module imports
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
project = "Google MCP Security"  # Modified
author = "Google Cloud Security"
copyright = f"{datetime.date.today().year}, {author}"

# The version info for the project you're documenting
try:
    # Attempt to get version from git, adjust path if necessary
    pipe = Popen("git describe --tags --always", stdout=PIPE, shell=True, cwd=os.path.abspath('../..')) # Added cwd
    git_version = pipe.stdout.read().decode("utf8").strip()

    if git_version:
        version = git_version.rsplit("-", 1)[0]
        release = git_version
    else:
        version = "0.1.0"
        release = "0.1.0"
except Exception:
    version = "0.1.0"
    release = "0.1.0"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here
extensions = [
    "myst_parser",           # Markdown support
    "sphinx_copybutton",     # Add copy buttons to code blocks
    "sphinx.ext.autodoc",    # API documentation
    "sphinx.ext.viewcode",   # Add links to view source code
    "sphinx.ext.napoleon",   # Support for Google-style docstrings
    "sphinx.ext.intersphinx", # Link to other projects' documentation
    "sphinx_click",         # Document click-based CLI applications
]

# MyST Parser configuration for extended Markdown support
myst_enable_extensions = [
    "colon_fence",           # Code blocks with colons
    "deflist",              # Definition lists
    "fieldlist",            # Field lists
    "html_admonition",      # HTML admonitions
    "html_image",           # HTML images
    "replacements",         # Text replacements
    "smartquotes",          # Smart quotes
    "tasklist",            # Task lists with checkboxes
]

# Support both .md and .rst files
source_suffix = [".rst", ".md"]

# The master toctree document
master_doc = "index"

# Add any paths that contain templates
templates_path = ["_templates"]

# Files to exclude from documentation build
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "venv",
    "env",
    "**/.git/**",
    "requirements.txt",
    "Makefile"
]

# Syntax highlighting style
pygments_style = "default"

# -- Options for HTML output -------------------------------------------------
html_theme = "furo"

# html_logo = "img/LogStory_logo.png"
html_logo = "img/SecOps-512-color.png"
html_favicon = "img/SecOps-32-color.png"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.

html_theme_options = {}
html_title = project

# Create _static directory if it doesn't exist
static_dir = os.path.join(os.path.dirname(__file__), '_static')
os.makedirs(static_dir, exist_ok=True)

# Set static paths for custom CSS/JS/images
html_static_path = ["_static", "img"]

# Theme options
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#1a73e8",    # Google Blue
        "color-brand-content": "#1a73e8",
    },
    "dark_css_variables": {
        "color-brand-primary": "#8ab4f8",    # Google Blue (dark mode)
        "color-brand-content": "#8ab4f8",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
    "announcement": "This is documentation for the Google MCP Security project.",
    "source_repository": "https://github.com/google/mcp-security/",
    "source_branch": "main",
    "source_directory": "docs/",
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/google/mcp-security",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
}

# -- Extension configurations ------------------------------------------------

# Intersphinx mapping to other projects
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'requests': ('https://requests.readthedocs.io/en/latest/', None),
}

# Napoleon settings for Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False

# Copy button settings
copybutton_prompt_text = "$ "
copybutton_prompt_is_regexp = True
copybutton_only_copy_prompt_lines = False
copybutton_remove_prompts = True

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "project-doc"


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "project.tex",
        project,
        author,
        "manual",
    )
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (
        master_doc,
        "project",
        project,
        [author],
        1,
    )
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "project",
        project,
        author,
        "project",
        "Documentation for {}".format(project),
        "Miscellaneous",
    )
]
