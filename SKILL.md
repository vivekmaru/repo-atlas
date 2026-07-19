---
name: repo-atlas
description: Create polished repository onboarding documentation as static HTML. Use when a user asks Codex to explore a repo, explain architecture, produce diagrams, render existing Markdown/spec docs into browser-friendly pages, build a glossary of acronyms/domain terms, summarize historical decisions from docs such as .kiro/, or make a new-engineer repo atlas/code map.
---

# Repo Atlas

## Goal

Build a reviewable static documentation bundle that helps a new engineer understand a repository quickly: what it does, how the main parts connect, which docs matter, what terms mean, and where to change code.

Default output path: `docs/repo-atlas/` unless the user asks otherwise.

## Non-Negotiable Output Contract

Unless the user explicitly asks for a smaller artifact, produce the full atlas shape below and keep it visually consistent:

- `index.html`: guided start page, not a marketing landing page.
- `architecture.html`: current architecture with diagrams.
- `history.html`: timeline and superseded decisions from repo docs.
- `operations.html`: build/run/deploy/observe/failure-mode guide.
- `code-map.html`: behavior-oriented source map, preferably interactive.
- `docs.html`: curated documentation shelf with summaries.
- `glossary.html`: grouped acronym/domain glossary.
- `read/*.html`: rendered important Markdown/spec documents.
- `styles.css`: use the bundled `assets/paper-atlas.css` starter unless the repo has a stronger design system or the user asks for another style.
- `vendor/fonts/*`: copy bundled Atkinson fonts when using the starter CSS.
- `vendor/mermaid.min.js`, `vendor/mermaid.LICENSE`, and `mermaid-render.js`: include when any reader page has Mermaid blocks.

Do not invent a new visual direction for each repo-atlas run. Start from the bundled warm paper technical-doc aesthetic, then adapt only where repo context or explicit user guidance requires it.

If a repo already contains a high-quality `docs/repo-atlas/`, use it as the local exemplar for structure, density, and tone before creating or regenerating pages.

## Workflow

1. **Gather context first**
   - Read repo entry points: `README*`, build files, package/workspace manifests, CI config, docs directories, and obvious app/service roots.
   - Search for decision/spec/history directories such as `.kiro/`, `docs/`, `adr/`, `architecture/`, `rfcs/`, `specs/`, and `design/`.
   - Use QMD or other local notes if project history is likely to matter and the environment provides it.
   - Inspect source by behavior, not only by directory tree: ingress, transformation, domain logic, persistence/transport, background jobs, operations, deployment, tests.

2. **Decide the atlas shape**
   - Prefer these pages: `index.html`, `architecture.html`, `history.html`, `operations.html`, `code-map.html`, `docs.html`, `glossary.html`, `styles.css`.
   - Add `read/*.html` pages for important Markdown/spec documents so browser links do not open raw Markdown.
   - If scope must be smaller, keep `index.html`, `architecture.html`, `code-map.html`, and `glossary.html`.
   - Do not stop at a file catalog. The atlas must explain relationships, flows, history, and common change paths.

3. **Use visual explanation**
   - Include diagrams before dense tables.
   - Show current architecture, request/data flow, deploy shape, and source-code ownership boundaries.
   - Mark historical/superseded diagrams clearly when including them.
   - Preserve Mermaid diagrams from source Markdown and render them in the browser. Do not leave `graph TB`, `sequenceDiagram`, `flowchart`, `classDiagram`, or `stateDiagram` blocks as raw code in reader pages.
   - For code maps, add an interactive layer when helpful: tabs for major views, clickable nodes, related-node highlighting, and a detail panel with role, files, docs, and common change reasons.

4. **Make docs readable in-browser**
   - Render important Markdown into static HTML under `read/`.
   - Add a short summary near the top of each rendered page.
   - Keep a source link back to the original Markdown.
   - Add local Mermaid support when rendered Markdown contains Mermaid blocks: use `scripts/fetch_mermaid.py` to vendor the pinned Mermaid bundle and license under `vendor/`, copy `assets/mermaid-render.js`, inject both scripts into reader pages, and verify diagrams render as SVG.
   - For less important Markdown, a styled docs index with summaries is enough.

5. **Build a glossary**
   - Extract acronyms, domain words, protocol names, vendor/product names, and operational abbreviations from docs and source.
   - Add `glossary.html` grouped by domain.
   - Add hover/focus explanations on first-use terms across the atlas using accessible text, not only visual decoration.

6. **Design for engineers, not marketing**
   - The first screen should be useful documentation, not a landing page.
   - Prefer restrained, tactile, information-dense pages.
   - Avoid generic blue/purple gradients, decorative blobs, and oversized card-heavy SaaS layouts.
   - Prefer a readable sans/mono pair for technical docs. The bundled starter uses Atkinson Hyperlegible Next and Atkinson Hyperlegible Mono; copy `assets/fonts/` into the output and keep the font paths local so `file://` viewing works.
   - Avoid editorial serif headings unless the user explicitly requests that style.
   - If the user supplied a style reference, follow it.
   - Use stable responsive dimensions so diagrams and buttons do not jump or overlap.

7. **Verify before finishing**
   - Run a static link sweep across the generated pages.
   - Run a local asset sweep for `src`, `href`, and CSS `url(...)`.
   - Start a local static server and inspect at least the index, code map, docs reader, and glossary.
   - Use a real browser for interactive diagrams and mobile layout.
   - If using Mermaid, verify a representative Mermaid diagram renders as SVG and loads the local vendored script.
   - If using bundled fonts, verify local font files load.
   - Remove temporary screenshots/browser metadata before final status.

## Resources

- Read `references/atlas-workflow.md` when planning or implementing a full atlas.
- Use `assets/paper-atlas.css` as a visual starter when no repo design system exists.
- Copy `assets/fonts/` when using the starter CSS, preserving the relative `vendor/fonts/*.woff2` output path or updating the CSS paths.
- Copy `assets/mermaid-render.js` when rendering Markdown pages that may contain Mermaid diagrams.
- Use `scripts/fetch_mermaid.py` to obtain the pinned local Mermaid bundle when it is needed. The script writes Mermaid's license beside the bundle.
- Use `scripts/render_markdown.py` to create simple static HTML reader pages for Markdown documents.

## Quality Bar

The result should answer these questions without making a new engineer reverse-engineer the repo:

- What is this system for?
- What are the main runtime components?
- What is the most important request/data flow?
- Which historical decisions matter, and which are superseded?
- Which docs/specs are canonical?
- What do the local acronyms and domain terms mean?
- Where do I change code for the common task categories?
