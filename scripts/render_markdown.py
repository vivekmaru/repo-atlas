#!/usr/bin/env python3
"""Render a Markdown file into a simple static HTML reader page.

This is intentionally small and dependency-free. It supports the Markdown
features most useful for repo docs: headings, paragraphs, unordered and ordered
lists, fenced code blocks, blockquotes, basic tables, inline code, emphasis,
strong text, and links.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


MERMAID_START = re.compile(
    r"^(%%\{[\s\S]*?\}%%\s*)?"
    r"(graph|flowchart|sequenceDiagram|classDiagram|stateDiagram|stateDiagram-v2|"
    r"erDiagram|gantt|journey|pie|gitGraph|mindmap|timeline|quadrantChart|"
    r"requirementDiagram|packet|sankey-beta|architecture-beta)\b"
)


def inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    return escaped


def render_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        cells = [inline(cell.strip()) for cell in line.strip().strip("|").split("|")]
        rows.append(cells)
    if not rows:
        return ""
    header = rows[0]
    body = rows[2:] if len(rows) > 1 and all(set(cell) <= {"-", ":"} for cell in rows[1]) else rows[1:]
    out = ["<table><thead><tr>"]
    out.extend(f"<th>{cell}</th>" for cell in header)
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>")
        out.extend(f"<td>{cell}</td>" for cell in row)
        out.append("</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def render_markdown(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    list_type: str | None = None
    code: list[str] | None = None
    table: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            out.append(f"<p>{inline(' '.join(paragraph))}</p>")
            paragraph = []

    def flush_list() -> None:
        nonlocal list_type
        if list_type:
            out.append(f"</{list_type}>")
            list_type = None

    def flush_table() -> None:
        nonlocal table
        if table:
            out.append(render_table(table))
            table = []

    for line in lines:
        if code is not None:
            if line.startswith("```"):
                source = chr(10).join(code)
                if MERMAID_START.match(source.strip()):
                    out.append(f"<pre class=\"mermaid\">{html.escape(source)}</pre>")
                else:
                    out.append(f"<pre><code>{html.escape(source)}</code></pre>")
                code = None
            else:
                code.append(line)
            continue

        if line.startswith("```"):
            flush_paragraph()
            flush_list()
            flush_table()
            code = []
            continue

        if not line.strip():
            flush_paragraph()
            flush_list()
            flush_table()
            continue

        if "|" in line and line.strip().startswith("|"):
            flush_paragraph()
            flush_list()
            table.append(line)
            continue
        flush_table()

        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            flush_paragraph()
            flush_list()
            level = len(heading.group(1))
            out.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            continue

        if line.startswith(">"):
            flush_paragraph()
            flush_list()
            out.append(f"<blockquote>{inline(line.lstrip('> ').strip())}</blockquote>")
            continue

        unordered = re.match(r"^\s*[-*]\s+(.*)$", line)
        ordered = re.match(r"^\s*\d+[.)]\s+(.*)$", line)
        if unordered or ordered:
            flush_paragraph()
            desired = "ul" if unordered else "ol"
            if list_type != desired:
                flush_list()
                out.append(f"<{desired}>")
                list_type = desired
            out.append(f"<li>{inline((unordered or ordered).group(1))}</li>")
            continue

        paragraph.append(line.strip())

    flush_paragraph()
    flush_list()
    flush_table()
    if code is not None:
        source = chr(10).join(code)
        if MERMAID_START.match(source.strip()):
            out.append(f"<pre class=\"mermaid\">{html.escape(source)}</pre>")
        else:
            out.append(f"<pre><code>{html.escape(source)}</code></pre>")
    return "\n".join(out)


def page(
    title: str,
    summary: str,
    source_href: str,
    body: str,
    css_href: str,
    mermaid_src: str | None,
    mermaid_render_src: str | None,
) -> str:
    scripts = ""
    if mermaid_src and mermaid_render_src:
        scripts = (
            f'\n    <script src="{html.escape(mermaid_src)}"></script>'
            f'\n    <script src="{html.escape(mermaid_render_src)}"></script>'
        )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{html.escape(title)}</title>
    <link rel="stylesheet" href="{html.escape(css_href)}">
  </head>
  <body>
    <main class="site-shell">
      <section class="hero">
        <p class="eyebrow">rendered source document</p>
        <h1>{html.escape(title)}</h1>
        <p class="lead">{html.escape(summary)}</p>
        <p><a href="{html.escape(source_href)}">Open source Markdown</a></p>
      </section>
      <article class="markdown-body">
{body}
      </article>
    </main>
    {scripts}
  </body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--title")
    parser.add_argument("--summary", default="Rendered from the source Markdown so it can be read comfortably in the browser.")
    parser.add_argument("--source-href")
    parser.add_argument("--css-href", default="../styles.css")
    parser.add_argument("--mermaid-src", help="Relative path to a local Mermaid browser bundle.")
    parser.add_argument("--mermaid-render-src", help="Relative path to the repo-atlas Mermaid adapter script.")
    args = parser.parse_args()

    markdown = args.source.read_text(encoding="utf-8")
    title = args.title or next(
        (line.lstrip("# ").strip() for line in markdown.splitlines() if line.startswith("#")),
        args.source.stem.replace("-", " ").title(),
    )
    source_href = args.source_href or str(args.source)
    body = render_markdown(markdown)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        page(
            title,
            args.summary,
            source_href,
            body,
            args.css_href,
            args.mermaid_src,
            args.mermaid_render_src,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
