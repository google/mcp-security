#!/usr/bin/env python3
# Copyright 2025 Google LLC
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
"""Renders the SVG diagrams embedded in docs/gti_workflows/*.md.

The diagrams use ``currentColor`` for every stroke and fill so they follow
the Furo light and dark themes without separate image variants.

Regenerate after editing:

    python3 docs/img/gti_workflows/render_diagrams.py
"""

import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT = "font-family=\"-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif\""
MONO = "font-family=\"SFMono-Regular, Menlo, Consolas, monospace\""


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

  def diamond(self, cx, cy, w, h, lines):
    pts = f"{cx},{cy - h/2} {cx + w/2},{cy} {cx},{cy + h/2} {cx - w/2},{cy}"
    self.parts.append(
        f'<polygon points="{pts}" fill="none" stroke="currentColor"'
        ' stroke-width="1.5"/>'
    )
    self._text_block(cx, cy, lines, mono=False)

  def _text_block(self, cx, cy, lines, mono):
    size = 12 if mono else 13
    family = MONO if mono else FONT
    total = len(lines) * (size + 4)
    start = cy - total / 2 + size
    for i, line in enumerate(lines):
      y = start + i * (size + 4)
      escaped = (
          line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
      )
      self.parts.append(
          f'<text x="{cx}" y="{y:.1f}" text-anchor="middle" font-size="{size}"'
          f' {family} fill="currentColor">{escaped}</text>'
      )

  def label(self, x, y, text, anchor="middle", size=12, italic=False):
    style = ' font-style="italic"' if italic else ""
    escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
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

  def line(self, points, dashed=True):
    dash = ' stroke-dasharray="4 4"' if dashed else ""
    pts = " ".join(f"{x},{y}" for x, y in points)
    self.parts.append(
        f'<polyline points="{pts}" fill="none" stroke="currentColor"'
        f' stroke-width="1" opacity="0.6"{dash}/>'
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


def render_scan_flow():
  c = Canvas(980, 860, "Non-blocking file scan flow with submit_file and get_analysis")
  cx = 300

  c.box(cx - 110, 20, 220, 44, ["Suspicious local file"], mono=False)
  c.arrow([(cx, 64), (cx, 96)])

  c.box(cx - 130, 96, 260, 44, ["get_file_report(hash)"])
  c.arrow([(cx, 140), (cx, 176)])

  c.diamond(cx, 216, 240, 80, ["Recent report", "already exists?"])
  c.label(cx + 130, 208, "yes: skip the upload", anchor="start")
  c.arrow([(cx + 120, 216), (940, 216), (940, 734), (884, 734)])

  c.label(cx - 10, 272, "no", anchor="end")
  c.arrow([(cx, 256), (cx, 292)])
  c.diamond(cx, 334, 260, 84, ["Authorized to share the", "file with the community?"])
  c.label(cx - 140, 326, "no", anchor="end")
  c.arrow([(cx - 130, 334), (cx - 200, 334)])
  c.box(40, 312, 60, 44, ["Stop"], mono=False, dashed=True)
  c.label(cx + 10, 390, "yes", anchor="start")
  c.arrow([(cx, 376), (cx, 412)])

  c.box(cx - 150, 412, 300, 52, ["submit_file(file_path)", "returns {id, type} at once"])
  c.arrow([(cx, 464), (cx, 500)])

  c.box(cx - 150, 500, 300, 52, ["get_analysis(analysis_id)", "include_engine_results=False"])
  c.arrow([(cx, 552), (cx, 588)])

  c.diamond(cx, 628, 220, 80, ["status ==", '"completed"?'])
  c.label(cx - 120, 620, "queued or in-progress:", anchor="end")
  c.label(cx - 120, 636, "poll again in 15 to 30 s", anchor="end", italic=True)
  c.arrow([(cx - 110, 628), (cx - 200, 628), (cx - 200, 526), (cx - 150, 526)])

  c.label(cx + 10, 684, "yes", anchor="start")
  c.arrow([(cx, 668), (cx, 698)])

  c.box(cx - 150, 698, 300, 44, ["Need per-engine names? (malicious 1 to 3)"], mono=False)
  c.arrow([(cx, 742), (cx, 772)])
  c.box(cx - 170, 772, 340, 52, ["get_analysis(analysis_id,", "include_engine_results=True)"])

  c.box(564, 698, 320, 72, [
      "Pivot on meta.file_info.sha256:",
      "get_file_behavior_summary(hash)",
      "get_entities_related_to_a_file(...)",
  ])
  c.arrow([(cx + 170, 798), (724, 798), (724, 770)])

  c.box(594, 412, 260, 72, [
      "analyse_file(file_path)",
      "blocking: waits for the scan",
      "to finish inside one tool call",
  ], dashed=True)
  c.line([(cx + 150, 438), (594, 438)])
  c.label(522, 430, "alternative", italic=True)
  c.arrow([(724, 484), (724, 698)], dashed=True)

  c.write("scan_flow.svg")


def render_agentic_session_lifecycle():
  c = Canvas(960, 640, "GTI Agentic session lifecycle across two analysts")

  # Swimlane headers
  c.label(240, 28, "Analyst A (session owner)", size=14)
  c.label(730, 28, "Analyst B (recipient)", size=14)
  c.line([(480, 10), (480, 630)])
  c.line([(20, 40), (940, 40)], dashed=False)

  ax = 240
  c.box(ax - 150, 60, 300, 52, ["ask_gti_agent(message)", "returns session_id + response"])
  c.arrow([(ax, 112), (ax, 148)])

  c.box(ax - 150, 148, 300, 52, ["continue_chat(session_id, message)", "repeat for each follow-up pivot"])
  c.arrow([(ax + 150, 174), (ax + 190, 174), (ax + 190, 130), (ax + 150, 130)])
  c.label(ax + 196, 158, "x N", anchor="start", italic=True)
  c.arrow([(ax, 200), (ax, 236)])

  c.box(ax - 170, 236, 340, 68, [
      "get_session_history(session_id)",
      "default: USER_MESSAGE + AGENT_FINAL_RESPONSE",
      "include_intermediate_events=True for traces",
  ])
  c.arrow([(ax, 304), (ax, 340)])

  c.box(ax - 150, 340, 300, 52, ["share_session(session_id)", "returns share_token"])
  c.arrow([(ax + 150, 366), (580, 366)])
  c.label(398, 352, "share_token via", anchor="start", size=11, italic=True)
  c.label(398, 386, "SOAR case comment", anchor="start", size=11, italic=True)

  bx = 730
  c.box(bx - 150, 340, 300, 52, ["copy_shared_session(share_token)", "returns a new session_id"])
  c.arrow([(bx, 392), (bx, 428)])
  c.box(bx - 150, 428, 300, 52, ["continue_chat(new_session_id, message)", "does not modify Analyst A's session"])

  c.arrow([(ax, 392), (ax, 428)])
  c.box(ax - 150, 428, 300, 52, ["list_sessions(limit=5)", "paginate with cursor"])
  c.arrow([(ax, 480), (ax, 516)])
  c.box(ax - 150, 516, 300, 52, ["delete_session(session_id)", "cleanup of finished sessions"], dashed=True)

  c.label(480, 610, "Each session_id is owned by the API key that created or copied it.", size=12, italic=True)

  c.write("agentic_session_lifecycle.svg")


def render_topology():
  c = Canvas(900, 330, "Local gti-mcp server versus hosted GTI Agentic MCP endpoint")

  c.box(30, 120, 200, 80, ["MCP client", "(Gemini CLI, Claude Desktop,", "ADK agent, IDE)"], mono=False)

  c.box(330, 40, 280, 96, [
      "Local gti-mcp (server/gti)",
      "uv run server.py + VT_APIKEY",
      "stdio transport",
      "50 tools",
  ])
  c.arrow([(230, 150), (330, 88)])

  c.box(330, 190, 280, 96, [
      "Hosted GTI Agentic MCP",
      "www.virustotal.com/api/v3/agentspace/mcp/",
      "Streamable HTTP + x-apikey header",
      "7 session tools",
  ])
  c.arrow([(230, 170), (330, 238)])

  c.box(690, 110, 190, 100, [
      "Google Threat Intelligence",
      "VirusTotal API v3",
      "GTI Enterprise, Enterprise+,",
      "or PoC Agentic entitlement",
  ], mono=False)
  c.arrow([(610, 88), (690, 140)])
  c.arrow([(610, 238), (690, 180)])

  c.label(450, 160, "pick one, or run both side by side", size=11, italic=True)
  c.label(450, 310, "Both paths authenticate with the same VT_APIKEY value.", size=12, italic=True)

  c.write("hosted_vs_local.svg")


if __name__ == "__main__":
  render_scan_flow()
  render_agentic_session_lifecycle()
  render_topology()
