# Coding Conventions

This document outlines the coding conventions for the Python code within the `google-mcp-security` project. The project aims to follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).

Code formatting and import sorting are enforced automatically using `pyink` and `isort`, respectively. These tools are configured in the `pyproject.toml` files within each server subdirectory and are run via `pre-commit` hooks and `Makefile` targets.

Key aspects enforced by the tools include:

*   **Line Length:** 88 characters (configured for both `pyink` and `isort`).
*   **Indentation:** 2 spaces is preferred for new work but 4 spaces is allowable for existing files. Do not mix within a file.
*   **Quotes:** Primarily double quotes (`"`), but `pyink` may adjust based on context.
*   **Imports:** Sorted according to the Google style profile in `isort`.
*   **Docstrings:** Use triple double quotes (`"""Docstring"""`). While not automatically formatted for content by `pyink`, follow Google style guide recommendations (e.g., for `Args:`, `Returns:`, `Raises:`).

While the tools handle most formatting, developers should still adhere to other aspects of the Google style guide, such as naming conventions and general best practices.
