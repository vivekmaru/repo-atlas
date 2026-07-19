# Repo Atlas Workflow Reference

## Reproducibility Notes

Repo atlas generation should be treated as a semi-deterministic documentation build, not open-ended web design.

- Start from `assets/paper-atlas.css`; do not create a new visual system unless the user asks.
- Copy bundled font assets and Mermaid adapter when needed. Use the bundled Mermaid fetch helper instead of an unpinned CDN URL.
- Keep the standard page set unless the user explicitly narrows scope.
- Prefer explicit summaries, source links, diagrams, glossary hovers, and change recipes over decorative layout work.
- If a prior atlas exists, inspect it first and preserve its strongest conventions.
- Different agents may otherwise produce different outputs because repo exploration, summarization, and UI composition are judgment-heavy tasks. Reduce that drift by following the output contract in `SKILL.md`.

## Discovery Checklist

Use fast local search first:

- `rg --files -g 'README*' -g '*.md' -g 'pom.xml' -g 'package.json' -g 'pnpm-workspace.yaml' -g 'go.mod' -g 'Cargo.toml' -g '*.sln' -g '.gitlab-ci.yml' -g 'github/workflows/*'`
- `rg -n "ADR|decision|architecture|spec|glossary|timeout|security|deploy|admin|API|protocol|migration|deprecated|superseded" .`
- `find . -maxdepth 3 -type d` when the repo structure is unfamiliar.

Then inspect the highest-signal files:

- build/workspace manifests
- CI/deploy configs
- docs/spec/history directories
- app entry points
- controllers/routes/handlers
- services/use cases/domain modules
- transports/clients/adapters
- persistence/config/infra modules
- tests that describe workflows

## Recommended Page Purposes

`index.html`
: Executive orientation. What exists, who uses it, current state, and where to start.

`architecture.html`
: Current runtime model. Include diagrams for request/data flow, component boundaries, state machines, and deployment shape.

`history.html`
: Timeline and decision record. Use source docs. Clearly label superseded plans and old diagrams.

`operations.html`
: How to build, run, observe, deploy, recover, and test failure modes.

`code-map.html`
: Visual source map. Explain code ownership by behavior, not folder tree. Include change recipes.

`docs.html`
: Documentation shelf. Summarize important Markdown/spec docs and link to rendered reader pages.

`glossary.html`
: Acronyms, domain terms, vendor/product names, protocol terms, and local abbreviations grouped by domain.

`read/*.html`
: Rendered Markdown pages with a summary, source link, and the original content styled for browser reading.

## Diagram Patterns

Use hand-authored HTML/CSS diagrams for atlas-native overview diagrams, but preserve and render existing diagram languages from source docs. If Markdown contains Mermaid fences, reader pages should render them as diagrams instead of showing raw Mermaid text.

Good diagram types:

- End-to-end flow: actor -> gateway -> service -> transport -> dependency.
- Component map: lanes for ingress, domain, transport, data, infra, observability.
- Mirror map: production component on one side, mock/simulator/test equivalent on the other.
- State model: lifecycle states and transitions with sources.
- Deployment shape: CI -> artifact store -> runtime stack -> external dependency.
- Change guide: user task -> files -> specs/tests.

For Mermaid in rendered Markdown:

- Detect fenced/code blocks starting with `graph`, `flowchart`, `sequenceDiagram`, `classDiagram`, `stateDiagram`, `stateDiagram-v2`, `erDiagram`, `gantt`, `journey`, `pie`, `gitGraph`, `mindmap`, `timeline`, `quadrantChart`, `requirementDiagram`, `packet`, `sankey-beta`, or `architecture-beta`.
- Convert those blocks to `<pre class="mermaid">...</pre>` before calling Mermaid, or use `assets/mermaid-render.js` to convert generated `<pre><code>...</code></pre>` blocks at runtime.
- Run `scripts/fetch_mermaid.py docs/repo-atlas/vendor/mermaid.min.js` to vendor the pinned Mermaid bundle and its `mermaid.LICENSE` file. This keeps direct `file://` viewing independent of a CDN.
- Inject scripts into reader pages using paths relative to `read/`: `../vendor/mermaid.min.js` and `../mermaid-render.js`.
- Style rendered Mermaid frames as scrollable paper panels; sequence diagrams can be wider than the viewport.

For interactive code maps:

- Keep static HTML/CSS/vanilla JS.
- Use tabs for major views.
- Use buttons for nodes so keyboard users can select them.
- On node selection, update a detail panel containing role, source files, related docs, and common change reasons.
- Highlight related nodes, but do not hide unrelated nodes by default.

## Glossary Extraction

Search docs and code for:

- all-caps tokens of 2+ characters
- vendor/product names
- protocol names
- domain nouns that appear in headings
- timer/state names
- config/env abbreviations
- payment/security/networking terms

Do not invent certainty for opaque terms. If a term is inferred from context, say so briefly.

Glossary entry shape:

- term
- expansion, if known
- plain-English meaning in this repo
- where it appears or why it matters

## Markdown Reader Pages

Render important Markdown into HTML when:

- the doc is canonical or near-canonical
- it contains architecture/spec/history/operations details
- raw Markdown in the browser would be hard to scan
- other atlas pages need to link to it often

Each reader page should have:

- title
- summary paragraph
- source Markdown link
- body rendered with headings, lists, tables, code blocks, blockquotes, and links
- local Mermaid rendering support when any Mermaid diagram blocks exist

## Typography

Prefer technical readability over editorial display type.

- Use a sans family for headings and body, not a serif default, unless the user asks for editorial styling.
- Use a distinct mono family for code, tags, paths, and metadata.
- The bundled starter CSS expects these output files:
  - `vendor/fonts/atkinson-hyperlegible-next-latin.woff2`
  - `vendor/fonts/atkinson-hyperlegible-mono-latin.woff2`
- If you use `assets/paper-atlas.css`, copy `assets/fonts/` to the output's `vendor/fonts/`, or adjust the CSS `@font-face` URLs.
- Avoid negative letter spacing and viewport-width font scaling; use stable sizes with media-query breakpoints.

## Verification

Minimum checks:

- link sweep: every local `href` points to an existing file
- asset sweep: every local `src` and CSS `url(...)` points to an existing file
- script syntax check if inline JS exists
- local static server
- browser check for index, code map, docs page, glossary, and one rendered reader page
- if Mermaid is present, verify a representative diagram renders as SVG and that Mermaid loads from the local vendored file
- verify font files load from local `vendor/fonts/`
- mobile viewport check for text overflow and diagram collapse
- `git status --short` after cleanup

If using screenshots, remove them unless the user asked to keep visual proof.
