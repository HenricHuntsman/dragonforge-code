# DragonForge Code Security Policy

DragonForge Code is an independently maintained, early-stage Go coding agent,
derived from the MIT-licensed OpenCode Go project. It has not received a full
security audit. This policy adapts the ideas of
[archived OpenCode PR #170](https://github.com/opencode-ai/opencode/pull/170)
without copying promises that cannot currently be substantiated.

## Supported versions

Development is focused on the latest `main` branch. Historical OpenCode
binaries mirrored under `upstream-*` are preserved artifacts and are **not**
supported or certified as secure DragonForge releases. No support lifetime
or vulnerability resolution SLA is currently promised.

## Reporting vulnerabilities

**Do not post sensitive exploit instructions, private data, API credentials,
or exploitable proof-of-concept code in public GitHub issues.**

Use [DragonForge's GitHub security advisory reporting page](https://github.com/HenricHuntsman/dragonforge-code/security/advisories)
when private vulnerability reporting is enabled. If that option is unavailable,
open a non-sensitive issue asking the repository maintainer to establish a
private reporting channel; do not include the vulnerability details publicly.

Useful report details include affected revision, operating system, component,
minimal safe reproducer, impact, and any suggested remediation. No public
disclosure time or response deadline is guaranteed.

## Current known boundaries and cautions

- **Tool permissions:** Interactive approval prompts do not form a filesystem
  sandbox. The shell tool's read-only classification is best-effort.
- **Noninteractive mode:** The inherited `--prompt` path currently calls
  `AutoApproveSession`, which can authorize operations without an interactive
  confirmation. Do not use unattended one-shot prompts against valuable or
  untrusted project files until this is fixed and tested.
- **Outbound requests:** The coding agent has network-capable tools, including
  Sourcegraph, web fetching and configured MCP endpoints. Selecting local
  Ollama does **not** automatically make every tool local-only.
- **Credentials:** Do not commit secrets to repositories, logs, session
  history or agent-accessible workspaces. Some provider integrations still
  accept cloud environment credentials.
- **Session storage:** Conversation/session information is stored in a local
  SQLite database. Encryption at rest has not been verified.
- **Tools and plugins:** Only use language servers, MCP executables and
  integrations from trusted sources. They may execute external processes.
- **N64 and TraceForge:** The supplied specialist launcher creates separate
  workspaces, but HOME configuration isolation is not OS-level containment.
  Never point an untrusted coding agent at original ROM collections or live
  TraceForge project files without explicit permission and backups.

## Maintainer security work

Follow [the security hardening issue](https://github.com/HenricHuntsman/dragonforge-code/issues/6)
for the noninteractive permission and network-tool review. Any fixes should
include focused negative tests, a reviewable pull request, and GitHub CI
verification before release.

## Upstream attribution

Original author and contributor credits remain in [LICENSE](LICENSE).
This policy is adapted from the intent of
[opencode-ai/opencode#170](https://github.com/opencode-ai/opencode/pull/170).
That archived proposal's original owner contact details, support schedules and
encryption claims do not apply to this independent fork.
