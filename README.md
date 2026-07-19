# Repo Atlas

[![skills.sh](https://skills.sh/b/vivekmaru/repo-atlas)](https://skills.sh/vivekmaru/repo-atlas)

A portable Agent Skill for turning an unfamiliar codebase into a static, browser-ready
onboarding atlas: architecture, history, operations, code map, docs shelf, and
a glossary.

## What it produces

By default, Repo Atlas builds a coherent documentation bundle under
`docs/repo-atlas/` in the target repository:

- guided start, architecture, history, operations, code-map, docs, and glossary pages
- browser-rendered versions of important Markdown and specification documents
- local fonts, diagrams, and assets that work from `file://` as well as a static host

It explains behavior and change paths rather than only listing directories.

## Demo

Repo Atlas generated this onboarding guide for the public
[Forge task-tracker repository](https://github.com/vivekmaru/task-tracker).

![Repo Atlas onboarding guide for Forge](examples/forge-atlas.jpg)

## Compatibility

Repo Atlas follows the open Agent Skills layout: one `SKILL.md` with standard
`name` and `description` frontmatter, plus relative scripts, references, and
assets. The same source works in Codex, Claude Code, and GitHub Copilot. The
Codex-specific interface metadata in `agents/openai.yaml` is optional and is
ignored by other runtimes.

The recommended installation method uses [skills.sh](https://www.skills.sh/docs),
which places the skill in each runtime's supported directory without creating
separate, drifting copies in this repository.

## Install

### Codex, Claude Code, and GitHub Copilot

Install for all three agent runtimes:

```bash
npx skills add vivekmaru/repo-atlas --skill repo-atlas \
  --global --agent codex claude-code github-copilot --yes
```

Omit `--global` to install it into the current project for your team. The
installer selects the shared Agent Skills directories supported by each runtime.

### Claude Code manually

```bash
git clone https://github.com/vivekmaru/repo-atlas.git ~/.claude/skills/repo-atlas
```

For a project-local install, clone it to `.claude/skills/repo-atlas` in the
target repository instead.

### GitHub Copilot manually

Clone the repository to `.github/skills/repo-atlas` in the target repository,
or to `~/.copilot/skills/repo-atlas` for a personal installation.

### With OpenSpec

OpenSpec is a planning layer, not a separate skill runtime. Initialize OpenSpec
for the agent you use, then install Repo Atlas alongside its generated skills:

```bash
openspec init --tools claude,github-copilot
npx skills add vivekmaru/repo-atlas --skill repo-atlas \
  --agent claude-code github-copilot --yes
```

Repo Atlas automatically includes `openspec/` specifications and change history
in its discovery pass. It coexists with OpenSpec's `.claude/skills/openspec-*`
and `.github/skills/openspec-*` directories; do not place it inside `openspec/`.

## Use

Ask the agent:

```text
Create a new-engineer HTML repo atlas for this repository.
```

The skill is self-contained apart from Python 3, which is used by the optional
Markdown renderer and Mermaid fetch helper.

## Mermaid bundle

Atlas pages with source Mermaid diagrams use a local browser bundle so they
continue to work offline. Repo Atlas intentionally does not commit the
third-party bundle. Instead, it pins Mermaid `11.16.0` and provides a helper
that verifies the npm tarball's SHA-512 integrity before extracting it:

```bash
python3 /path/to/repo-atlas/scripts/fetch_mermaid.py \
  docs/repo-atlas/vendor/mermaid.min.js
```

The helper also writes Mermaid's MIT license beside the bundle. Use it only
when the generated atlas contains Mermaid diagrams.

## License

Repo Atlas is available under the [MIT License](LICENSE). Bundled font notices
are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
