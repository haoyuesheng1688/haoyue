# Haoyue Skill and Knowledge Index

Remote repository: `haoyuesheng1688/haoyue`

Default branch: `main`

## Operating Contract

- Source of truth: GitHub remote content.
- Required read-before-write: fetch the target file before creating, updating, or deleting it.
- Required index update: every new skill or knowledge domain must update this file.
- Required keyword discipline: every entry must include searchable keywords, tags, variables, API names, or software names.
- Required validation note: every publish should include the smallest useful validation evidence or clear validation boundary.

## Skills

No skills have been published yet.

### Skill Entry Format

```text
- skills/<skill-name>/
  - Purpose: <what this skill enables>
  - Keywords: <software, API, variables, tags, project names>
  - Validation: <small-case test or verified boundary>
  - Updated: YYYY-MM-DD
```

## Knowledge Bases

No knowledge domains have been published yet.

### Knowledge Entry Format

```text
- knowledge/<domain>/
  - Purpose: <what this knowledge base captures>
  - Keywords: <software, API, variables, tags, project names>
  - Validation: <read-back, screenshot, command evidence, or boundary>
  - Updated: YYYY-MM-DD
```

## Reserved Top-Level Paths

- `skills/`: reusable Codex skills.
- `knowledge/`: engineering knowledge bases and operational references.
- `INDEX.md`: authoritative remote index.
- `README.md`: repository contract and structure.
- `.gitignore`: local artifact and secret exclusion rules.
