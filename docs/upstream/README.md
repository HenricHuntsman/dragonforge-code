# Historical OpenCode archive

Source: https://github.com/opencode-ai/opencode. Catalog captured 18 October 2026, Melbourne.

This is a historical preservation collection, separate from new DragonForge builds. Original author and contributor credits and licence notices remain in force. The source repository is archived; these copies do not imply endorsement or renewed maintenance by its original authors.

## Coverage

- 50 releases and 504 original attached assets (6,203,322,140 bytes, approximately 6.2 GB).
- 25 branch tips, exact tag refs, and 42 open-PR records with source references.
- The reviewed release metadata is saved alongside each mirrored release, with computed SHA-256 digests and a link to the full upstream API record.
- Source commit ancestry is already imported into DragonForge. The recovery branches preserved in HenricHuntsman/opencode remain distinct from production code.

The catalog is a snapshot, not a complete copy of GitHub's website: issues, comments, reviews, discussions, account information, settings, stars and other service records are not all mirrored. Existing source links remain authoritative for those records.

## Historical release copies

Each original release is copied under an `upstream-` tag. Existing archive tags can point to the original commit. New archive tags point to the preservation snapshot so historical workflow files do not require additional token permissions. Exact original source tar/zip archives are attached to every historical release, and its original commit is recorded. It is named Historical OpenCode, does not become the latest DragonForge release, and retains upstream release notes and source links. Use the attached upstream-source archives: GitHub's automatic Source code links may refer to the preservation snapshot. The newest historical copy also includes upstream-history.bundle, containing all upstream branches and tags, including disconnected release history.

The import checks the reviewed inventory against live upstream metadata, downloaded sizes, GitHub-provided SHA-256 digests and entries in checksums.txt when available. Every upload is verified against the destination's digest. Existing conflicting assets or tag targets stop the import. An interrupted release remains a draft until complete; a rerun reuses verified assets. API rate limits and temporary gateway failures are retried; permission failures stop with the GitHub error message.

Historical copies are preserved binaries, not runtime-certified builds. No new security or compatibility guarantee is implied.

## Run and maintain

The Preserve historical upstream releases workflow runs when its workflow or importer changes on main or the dedicated archive branch, and supports manual reruns. It uses the destination repository's scoped Actions token; no token is stored in source. Allow up to three hours for the full import. Inspect its result before calling the mirror complete.

Local inventory-only check (no network or writes):

```sh
python3 tests/test_upstream_archive.py
python3 scripts/mirror_upstream_releases.py
```

Publishing is restricted to the DragonForge workflow environment. The default local command never publishes.

## Release inventory

| Original release | Published | Files | Historical copy |
| --- | --- | ---: | --- |
| [v0.0.55](https://github.com/opencode-ai/opencode/releases/tag/v0.0.55) | 2025-06-27 | 9 | [upstream-v0.0.55](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.55) |
| [v0.0.54](https://github.com/opencode-ai/opencode/releases/tag/v0.0.54) | 2025-06-25 | 9 | [upstream-v0.0.54](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.54) |
| [v0.0.53](https://github.com/opencode-ai/opencode/releases/tag/v0.0.53) | 2025-06-07 | 9 | [upstream-v0.0.53](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.53) |
| [v0.0.52](https://github.com/opencode-ai/opencode/releases/tag/v0.0.52) | 2025-06-07 | 9 | [upstream-v0.0.52](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.52) |
| [v0.0.51](https://github.com/opencode-ai/opencode/releases/tag/v0.0.51) | 2025-06-04 | 9 | [upstream-v0.0.51](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.51) |
| [v0.0.50](https://github.com/opencode-ai/opencode/releases/tag/v0.0.50) | 2025-06-04 | 9 | [upstream-v0.0.50](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.50) |
| [v0.0.49](https://github.com/opencode-ai/opencode/releases/tag/v0.0.49) | 2025-05-22 | 9 | [upstream-v0.0.49](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.49) |
| [v0.0.48](https://github.com/opencode-ai/opencode/releases/tag/v0.0.48) | 2025-05-22 | 9 | [upstream-v0.0.48](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.48) |
| [v0.0.47](https://github.com/opencode-ai/opencode/releases/tag/v0.0.47) | 2025-05-21 | 9 | [upstream-v0.0.47](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.47) |
| [v0.0.46](https://github.com/opencode-ai/opencode/releases/tag/v0.0.46) | 2025-05-14 | 9 | [upstream-v0.0.46](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.46) |
| [v0.0.45](https://github.com/opencode-ai/opencode/releases/tag/v0.0.45) | 2025-05-14 | 9 | [upstream-v0.0.45](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.45) |
| [v0.0.44](https://github.com/opencode-ai/opencode/releases/tag/v0.0.44) | 2025-05-09 | 9 | [upstream-v0.0.44](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.44) |
| [v0.0.43](https://github.com/opencode-ai/opencode/releases/tag/v0.0.43) | 2025-05-09 | 9 | [upstream-v0.0.43](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.43) |
| [v0.0.42](https://github.com/opencode-ai/opencode/releases/tag/v0.0.42) | 2025-05-09 | 9 | [upstream-v0.0.42](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.42) |
| [v0.0.40](https://github.com/opencode-ai/opencode/releases/tag/v0.0.40) | 2025-05-02 | 9 | [upstream-v0.0.40](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.40) |
| [v0.0.39](https://github.com/opencode-ai/opencode/releases/tag/v0.0.39) | 2025-05-01 | 9 | [upstream-v0.0.39](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.39) |
| [v0.0.38](https://github.com/opencode-ai/opencode/releases/tag/v0.0.38) | 2025-05-01 | 9 | [upstream-v0.0.38](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.38) |
| [v0.0.37](https://github.com/opencode-ai/opencode/releases/tag/v0.0.37) | 2025-05-01 | 9 | [upstream-v0.0.37](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.37) |
| [v0.0.36](https://github.com/opencode-ai/opencode/releases/tag/v0.0.36) | 2025-04-29 | 9 | [upstream-v0.0.36](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.36) |
| [v0.0.35](https://github.com/opencode-ai/opencode/releases/tag/v0.0.35) | 2025-04-28 | 9 | [upstream-v0.0.35](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.35) |
| [v0.0.34](https://github.com/opencode-ai/opencode/releases/tag/v0.0.34) | 2025-04-27 | 9 | [upstream-v0.0.34](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.34) |
| [v0.0.33](https://github.com/opencode-ai/opencode/releases/tag/v0.0.33) | 2025-04-27 | 9 | [upstream-v0.0.33](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.33) |
| [v0.0.32](https://github.com/opencode-ai/opencode/releases/tag/v0.0.32) | 2025-04-27 | 9 | [upstream-v0.0.32](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.32) |
| [v0.0.31](https://github.com/opencode-ai/opencode/releases/tag/v0.0.31) | 2025-04-27 | 9 | [upstream-v0.0.31](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.31) |
| [v0.0.30](https://github.com/opencode-ai/opencode/releases/tag/v0.0.30) | 2025-04-27 | 9 | [upstream-v0.0.30](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.30) |
| [v0.0.29](https://github.com/opencode-ai/opencode/releases/tag/v0.0.29) | 2025-04-27 | 9 | [upstream-v0.0.29](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.29) |
| [v0.0.28](https://github.com/opencode-ai/opencode/releases/tag/v0.0.28) | 2025-04-27 | 9 | [upstream-v0.0.28](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.28) |
| [v0.0.27](https://github.com/opencode-ai/opencode/releases/tag/v0.0.27) | 2025-04-26 | 9 | [upstream-v0.0.27](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.27) |
| [v0.0.26](https://github.com/opencode-ai/opencode/releases/tag/v0.0.26) | 2025-04-24 | 9 | [upstream-v0.0.26](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.26) |
| [v0.0.24](https://github.com/opencode-ai/opencode/releases/tag/v0.0.24) | 2025-04-24 | 9 | [upstream-v0.0.24](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.24) |
| [v0.0.21](https://github.com/opencode-ai/opencode/releases/tag/v0.0.21) | 2025-04-24 | 9 | [upstream-v0.0.21](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.21) |
| [v0.0.20](https://github.com/opencode-ai/opencode/releases/tag/v0.0.20) | 2025-04-24 | 9 | [upstream-v0.0.20](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.20) |
| [v0.0.19](https://github.com/opencode-ai/opencode/releases/tag/v0.0.19) | 2025-04-24 | 12 | [upstream-v0.0.19](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.19) |
| [v0.0.18](https://github.com/opencode-ai/opencode/releases/tag/v0.0.18) | 2025-04-24 | 12 | [upstream-v0.0.18](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.18) |
| [v0.0.17](https://github.com/opencode-ai/opencode/releases/tag/v0.0.17) | 2025-04-23 | 12 | [upstream-v0.0.17](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.17) |
| [v0.0.16](https://github.com/opencode-ai/opencode/releases/tag/v0.0.16) | 2025-04-23 | 12 | [upstream-v0.0.16](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.16) |
| [v0.0.15](https://github.com/opencode-ai/opencode/releases/tag/v0.0.15) | 2025-04-23 | 12 | [upstream-v0.0.15](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.15) |
| [v0.0.14](https://github.com/opencode-ai/opencode/releases/tag/v0.0.14) | 2025-04-23 | 12 | [upstream-v0.0.14](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.14) |
| [v0.0.13](https://github.com/opencode-ai/opencode/releases/tag/v0.0.13) | 2025-04-23 | 12 | [upstream-v0.0.13](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.13) |
| [v0.0.12](https://github.com/opencode-ai/opencode/releases/tag/v0.0.12) | 2025-04-23 | 12 | [upstream-v0.0.12](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.12) |
| [v0.0.11](https://github.com/opencode-ai/opencode/releases/tag/v0.0.11) | 2025-04-23 | 12 | [upstream-v0.0.11](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.11) |
| [v0.0.10](https://github.com/opencode-ai/opencode/releases/tag/v0.0.10) | 2025-04-22 | 12 | [upstream-v0.0.10](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.10) |
| [v0.0.9](https://github.com/opencode-ai/opencode/releases/tag/v0.0.9) | 2025-04-22 | 12 | [upstream-v0.0.9](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.9) |
| [v0.0.7](https://github.com/opencode-ai/opencode/releases/tag/v0.0.7) | 2025-04-22 | 12 | [upstream-v0.0.7](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.7) |
| [v0.0.6](https://github.com/opencode-ai/opencode/releases/tag/v0.0.6) | 2025-04-22 | 12 | [upstream-v0.0.6](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.6) |
| [v0.0.5](https://github.com/opencode-ai/opencode/releases/tag/v0.0.5) | 2025-04-22 | 12 | [upstream-v0.0.5](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.5) |
| [v0.0.4](https://github.com/opencode-ai/opencode/releases/tag/v0.0.4) | 2025-04-22 | 12 | [upstream-v0.0.4](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.4) |
| [v0.0.3](https://github.com/opencode-ai/opencode/releases/tag/v0.0.3) | 2025-04-22 | 12 | [upstream-v0.0.3](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.3) |
| [v0.0.2](https://github.com/opencode-ai/opencode/releases/tag/v0.0.2) | 2025-04-22 | 12 | [upstream-v0.0.2](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.2) |
| [v0.0.1](https://github.com/opencode-ai/opencode/releases/tag/v0.0.1) | 2025-04-22 | 12 | [upstream-v0.0.1](https://github.com/HenricHuntsman/dragonforge-code/releases/tag/upstream-v0.0.1) |
