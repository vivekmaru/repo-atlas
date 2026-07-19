# Repo Atlas

A Codex skill for turning an unfamiliar codebase into a static, browser-ready
onboarding atlas: architecture, history, operations, code map, docs shelf, and
a glossary.

## What it produces

By default, Repo Atlas builds a coherent documentation bundle under
`docs/repo-atlas/` in the target repository:

- guided start, architecture, history, operations, code-map, docs, and glossary pages
- browser-rendered versions of important Markdown and specification documents
- local fonts, diagrams, and assets that work from `file://` as well as a static host

It explains behavior and change paths rather than only listing directories.

## Install

Clone the repository into Codex's skills directory:

```bash
git clone https://github.com/vivekmaru/repo-atlas.git "${CODEX_HOME:-$HOME/.codex}/skills/repo-atlas"
```

Then ask Codex:

```text
Use $repo-atlas to explore this repository and create a new-engineer HTML repo atlas.
```

The skill is self-contained apart from Python 3, which is used by the optional
Markdown renderer and Mermaid fetch helper.

## Mermaid bundle

Atlas pages with source Mermaid diagrams use a local browser bundle so they
continue to work offline. Repo Atlas intentionally does not commit the
third-party bundle. Instead, it pins Mermaid `11.16.0` and provides a helper
that verifies the npm tarball's SHA-512 integrity before extracting it:

```bash
python3 /path/to/repo-atlas/scripts/fetch_mermaid.py \\
  docs/repo-atlas/vendor/mermaid.min.js
```

The helper also writes Mermaid's MIT license beside the bundle. Use it only
when the generated atlas contains Mermaid diagrams.

## License

Repo Atlas is available under the [MIT License](LICENSE). Bundled font notices
are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
