# ChatGPT Skills Library

A reduced, higher-signal library of agent skills for ChatGPT. The repo now favors fewer, broader skills with real deterministic tooling over a long tail of thin utility wrappers.

## Structure

Each skill lives in its own folder and contains:

- `SKILL.md`: frontmatter plus operational instructions
- `agents/openai.yaml`: UI-facing metadata for skill pickers
- `scripts/`: executable helpers and `requirements.txt` when Python scripts exist
- `references/`: load-on-demand documentation when needed
- `assets/`: templates or static resources used in outputs

## Core Commands

```bash
python3 skill-creator/scripts/init_skill.py my-skill --path .
python3 skill-creator/scripts/generate_openai_yaml.py my-skill \
  --interface display_name="My Skill" \
  --interface short_description="One-line summary" \
  --interface default_prompt="Help me use this skill."
python3 skill-creator/scripts/quick_validate.py my-skill
python3 audit_all_skills.py
python3 verify_docs.py
python3 skill-creator/scripts/package_skill.py my-skill ./dist
```

## Current Catalog

<!-- SKILL-LIST:START -->
- `crypto-ta-analyzer`
- `data-storyteller`
- `document-converter-suite`
- `financial-calculator`
- `geo-toolkit`
- `image-enhancement-suite`
- `media-toolkit`
- `mcp-builder`
- `ocr-document-processor`
- `qr-code-generator`
- `skill-creator`
- `svg-precision-skill`
<!-- SKILL-LIST:END -->

## Notes

- GitHub Actions runs structural validation, catalog checks, and the dependency-free repository tests on pull requests and pushes to `main`.
- Structural checks do not establish runtime correctness or the vulnerability status of optional dependencies.
- The old micro-skill catalog was intentionally pruned.
- Overlapping image, media, geo, and analytics utilities were merged into broader suites.
- Repo docs are verified against the actual skill folders with `verify_docs.py`.
