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

Uses an explicit self-contained dark-slate palette rather than ``currentColor``
because Sphinx and GitHub embed Markdown images as external ``<img>`` documents
that do not inherit host HTML ``color`` styles across light and dark themes.

Regenerate after editing:

    python3 docs/img/gti_remote/render_diagrams.py
"""

import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT = 'font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif"'
MONO = 'font-family="SFMono-Regular, Menlo, Consolas, monospace"'

BACKDROP_FILL = "#0f172a"
BACKDROP_STROKE = "#334155"
CARD_FILL = "#1e293b"
REMOTE_BORDER = "#94a3b8"
LOCAL_BORDER = "#64748b"
PRIMARY_TEXT = "#f8fafc"
SECONDARY_TEXT = "#e2e8f0"
CAPTION_AND_LINE = "#cbd5e1"
ARROWHEAD_FILL = "#93c5fd"


def _escape(text: str) -> str:
  return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class Canvas:
  """Collects SVG fragments and writes a self-contained accessible SVG file."""

  def __init__(self, width: int, height: int, title: str):
    self.width = width
    self.height = height
    self.title = title
    self.parts: list[str] = [
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="12"'
        f' fill="{BACKDROP_FILL}" stroke="{BACKDROP_STROKE}"'
        ' stroke-width="1.5"/>'
    ]

  def box(self, x, y, w, h, lines, mono=True, dashed=False, radius=6):
    stroke = LOCAL_BORDER if dashed else REMOTE_BORDER
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    self.parts.append(
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}"'
        f' fill="{CARD_FILL}" stroke="{stroke}" stroke-width="1.5"{dash}/>'
    )
    self._text_block(x + w / 2, y + h / 2, lines, mono)

  def _text_block(self, cx, cy, lines, mono):
    size = 12 if mono else 13
    family = MONO if mono else FONT
    total = len(lines) * (size + 5)
    start = cy - total / 2 + size
    for i, line in enumerate(lines):
      y = start + i * (size + 5)
      fill = PRIMARY_TEXT if i == 0 else SECONDARY_TEXT
      weight = ' font-weight="600"' if i == 0 else ""
      escaped = _escape(line)
      self.parts.append(
          f'<text x="{cx}" y="{y:.1f}" text-anchor="middle" font-size="{size}"'
          f' {family}{weight} fill="{fill}">{escaped}</text>'
      )

  def label(self, x, y, text, anchor="middle", size=12, italic=False):
    style = ' font-style="italic"' if italic else ""
    escaped = _escape(text)
    self.parts.append(
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}"'
        f' {FONT}{style} fill="{CAPTION_AND_LINE}">{escaped}</text>'
    )

  def arrow(self, points, dashed=False):
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    pts = " ".join(f"{x},{y}" for x, y in points)
    self.parts.append(
        f'<polyline points="{pts}" fill="none" stroke="{CAPTION_AND_LINE}"'
        f' stroke-width="1.5" marker-end="url(#arrow)"{dash}/>'
    )

  def write(self, filename: str):
    body = "\n  ".join(self.parts)
    escaped_title = _escape(self.title)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" role="img" aria-labelledby="title">
  <title id="title">{escaped_title}</title>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{ARROWHEAD_FILL}"/>
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
      840,
      464,
      "Comparison of Remote GTI Agentic MCP, VirusTotal AI Hosted MCP, and local gti-mcp",
  )

  c.box(
      18,
      169,
      196,
      110,
      [
          "MCP client",
          "Gemini CLI, Antigravity,",
          "Goose, Claude Code, Codex,",
          "Cursor, VS Code, ADK",
      ],
      mono=False,
  )

  # Lane 1: Remote GTI Agentic MCP
  c.box(
      256,
      24,
      328,
      108,
      [
          "Remote GTI Agentic MCP (gti-agentic)",
          "www.virustotal.com/api/v3/agentspace/mcp/",
          "Stateless Streamable HTTP + x-apikey",
          "7 specialist-agent session tools",
      ],
  )
  c.arrow([(214, 196), (256, 78)])
  c.box(
      620,
      24,
      202,
      108,
      [
          "GTI Agentic platform",
          "Server-side threat and",
          "malware specialist agents",
          "GTI Enterprise / Plus / PoC",
      ],
      mono=False,
  )
  c.arrow([(584, 78), (620, 78)])

  # Lane 2: VirusTotal AI Hosted MCP
  c.box(
      256,
      170,
      328,
      108,
      [
          "VirusTotal AI Hosted MCP (virustotal)",
          "ai.virustotal.com/mcp",
          "Streamable HTTP + Browser OAuth 2.1",
          "Direct IP, file, domain, URL reports",
      ],
  )
  c.arrow([(214, 224), (256, 224)])
  c.box(
      620,
      170,
      202,
      108,
      [
          "VirusTotal AI service",
          "OAuth sign-in (no API key)",
          "Lookup and scan tools",
          "Published free-tier quota",
      ],
      mono=False,
  )
  c.arrow([(584, 224), (620, 224)])

  # Lane 3: Local open-source gti-mcp
  c.box(
      256,
      316,
      328,
      108,
      [
          "Local GTI MCP server (gti)",
          "uvx gti_mcp + VT_APIKEY",
          "Local stdio Python process",
          "35+ direct VirusTotal API v3 tools",
      ],
      dashed=True,
  )
  c.arrow([(214, 252), (256, 370)], dashed=True)
  c.box(
      620,
      316,
      202,
      108,
      [
          "GTI / VirusTotal API v3",
          "Collections, DTM, standard",
          "YARA rulesets, Threat",
          "Profiles, IoC graphs",
      ],
      mono=False,
  )
  c.arrow([(584, 370), (620, 370)], dashed=True)

  c.label(
      420,
      448,
      "Register one endpoint or run multiple servers side by side under distinct server keys.",
      size=12,
      italic=True,
  )

  c.write("gti_remote_vs_local.svg")


if __name__ == "__main__":
  render_remote_vs_local()
