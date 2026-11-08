#!/usr/bin/env python3
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Renders the SVG diagram embedded in docs/gti_remote_server.md.

Uses ``currentColor`` for every stroke and fill so one SVG adapts cleanly
to both Furo light and dark themes.

Regenerate after editing:

    python3 docs/img/gti_remote/render_diagrams.py
"""

import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT = 'font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif"'
MONO = 'font-family="SFMono-Regular, Menlo, Consolas, monospace"'


class Canvas:
  """Collects SVG fragments and writes a theme-neutral SVG file."""

  def __init__(self, width: int, height: int, title: str):
    self.width = width
    self.height = height
    self.title = title
    self.parts: list[str] = []

  def box(self, x, y, w, h, lines, mono=True, dashed=False, radius=6):
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    self.parts.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}"'
        f' fill="none" stroke="currentColor" stroke-width="1.5"{dash}/>'
    )
    self._text_block(x + w / 2, y + h / 2, lines, mono)

  def _text_block(self, cx, cy, lines, mono):
    size = 12 if mono else 13
    family = MONO if mono else FONT
    total = len(lines) * (size + 5)
    start = cy - total / 2 + size
    for i, line in enumerate(lines):
      y = start + i * (size + 5)
      escaped = (
          line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
      )
      self.parts.append(
          f'<text x="{cx}" y="{y:.1f}" text-anchor="middle" font-size="{size}"'
          f' {family} fill="currentColor">{escaped}</text>'
      )

  def label(self, x, y, text, anchor="middle", size=12, italic=False):
    style = ' font-style="italic"' if italic else ""
    escaped = (
        text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )
    self.parts.append(
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}"'
        f' {FONT}{style} fill="currentColor">{escaped}</text>'
    )

  def arrow(self, points, dashed=False):
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    pts = " ".join(f"{x},{y}" for x, y in points)
    self.parts.append(
        f'<polyline points="{pts}" fill="none" stroke="currentColor"'
        f' stroke-width="1.5" marker-end="url(#arrow)"{dash}/>'
    )

  def write(self, filename: str):
    body = "\n  ".join(self.parts)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" role="img" aria-labelledby="title">
  <title id="title">{self.title}</title>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/>
    </marker>
  </defs>
  {body}
</svg>
"""
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
      f.write(svg)
    print(f"wrote {path}")


def render_remote_vs_local():
  c = Canvas(
      940,
      340,
      "Remote GTI Agentic MCP endpoint versus local gti-mcp server",
  )

  c.box(
      24,
      115,
      216,
      96,
      [
          "MCP client",
          "Gemini CLI, Antigravity,",
          "Goose, Claude Code,",
          "Cursor, VS Code, ADK",
      ],
      mono=False,
  )

  c.box(
      316,
      32,
      320,
      104,
      [
          "Remote GTI Agentic MCP (gti-agentic)",
          "www.virustotal.com/api/v3/agentspace/mcp/",
          "Streamable HTTP + x-apikey header",
          "7 stateful session tools",
      ],
  )
  c.arrow([(240, 148), (316, 84)])

  c.box(
      316,
      190,
      320,
      104,
      [
          "Local GTI MCP server (gti-mcp)",
          "uvx gti_mcp + VT_APIKEY",
          "stdio transport",
          "Direct VirusTotal API v3 tools",
      ],
      dashed=True,
  )
  c.arrow([(240, 178), (316, 242)], dashed=True)

  c.box(
      712,
      32,
      204,
      104,
      [
          "GTI Agentic platform",
          "Specialist threat and",
          "malware agents",
          "Enterprise / Plus license",
      ],
      mono=False,
  )
  c.arrow([(636, 84), (712, 84)])

  c.box(
      712,
      190,
      204,
      104,
      [
          "Google Threat Intelligence",
          "VirusTotal API v3",
          "Collections, files, rules,",
          "domains, IPs, and URLs",
      ],
      mono=False,
  )
  c.arrow([(636, 242), (712, 242)], dashed=True)
  c.arrow([(814, 136), (814, 190)])

  c.label(
      476,
      166,
      "Run either option, or register both side by side",
      size=12,
      italic=True,
  )
  c.label(
      470,
      322,
      "Both options authenticate with the same Google Threat Intelligence API key.",
      size=12,
      italic=True,
  )

  c.write("gti_remote_vs_local.svg")


if __name__ == "__main__":
  render_remote_vs_local()
