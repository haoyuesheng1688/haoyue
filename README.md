# haoyue

`haoyuesheng1688/haoyue` is the remote-first repository for reusable Codex skills and engineering knowledge bases.

## Repository Contract

- This GitHub repository is the publishing target for future generated skills and knowledge bases.
- Do not treat any local checkout as the source of truth unless a task explicitly says to sync from it.
- Prefer GitHub connector or GitHub Contents API reads before every write.
- Keep runtime state, secrets, local caches, virtual environments, and temporary logs out of the repository.

## Directory Layout

```text
skills/
  <skill-name>/
    SKILL.md
    agents/openai.yaml        # optional
    scripts/                  # optional deterministic helpers
    references/               # optional loaded-on-demand knowledge
    assets/                   # optional output resources

knowledge/
  <domain>/
    README.md or <domain>-index.md
    references/               # optional source notes
    evidence/                 # optional sanitized proof artifacts
```

## Publishing Rules

- Every skill must include `skills/<skill-name>/SKILL.md` with valid YAML frontmatter.
- Every knowledge domain must include an entry file and clear keywords.
- Every new or updated skill and knowledge domain must be registered in `INDEX.md`.
- Prefer small-case validation before larger automation or architecture work.
- Record key variables, tags, API names, software connection paths, validation evidence, and known failure modes.

## Current Status

Initialized as an empty remote-first host for future skills and knowledge bases.
