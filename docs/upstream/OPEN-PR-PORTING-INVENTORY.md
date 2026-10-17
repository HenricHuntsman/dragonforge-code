# Archived OpenCode: unmerged PRs and branch tips

Source: [opencode-ai/opencode](https://github.com/opencode-ai/opencode) (archived). Inventory checked 2026-10-18. This is a **reference and porting backlog**, not code merged into DragonForge.

The archived original has **42 open pull requests** and **25 branch tips** in this snapshot. The main-line tracked source files and Git ancestry are already present in DragonForge. For historical release assets and checksums, see [the release-preservation catalogue](README.md).

## Porting policy

- Keep original contributors, PR links and MIT licence/copyright attribution.
- Do **not** mass-merge archived 2025 PRs: they may conflict with the renamed module, newer APIs, Ollama support, Go dependencies or security policy.
- Port each change into an independent DragonForge branch, add current tests, review security and GitHub CI, then merge if useful. Preserve the original PR's link in the new PR.
- Keep source branch tip hashes as reference pointers. Listing a hash here does **not** import that branch's commits or guarantee its objects are reachable in DragonForge.
- Preserve review/discussion metadata by linking to GitHub; issues, comments and cross-repository PR records cannot be transferred faithfully by copying source files.

## High-value triage

| Upstream | Candidate | Disposition |
|---|---|---|
| [#281](https://github.com/opencode-ai/opencode/pull/281) | Empty MCP arguments | Adapted in [DragonForge #4](https://github.com/HenricHuntsman/dragonforge-code/pull/4); validate CI before merge |
| [#167](https://github.com/opencode-ai/opencode/pull/167) | Privacy prompts and external search protection | Security audit needed; original patch includes incompatible imports, do **not** cherry-pick |
| [#346](https://github.com/opencode-ai/opencode/pull/346) | Ollama and extended providers | Compare to DragonForge's existing local model discovery; large overlapping patch, no direct merge |
| [#245](https://github.com/opencode-ai/opencode/pull/245) | Custom provider endpoints/headers | Review threat model and per-project configuration first |
| [#294](https://github.com/opencode-ai/opencode/pull/294) | Copilot authentication | Needs current 2026 token/OAuth validation; don't import tokens into test fixtures |
| [#243](https://github.com/opencode-ai/opencode/pull/243) | Session delete UI, LiteLLM | Separate session safety from provider integration |
| [#249](https://github.com/opencode-ai/opencode/pull/249), [#250](https://github.com/opencode-ai/opencode/pull/250) | Dependency automation and linter | Update to current dependencies, permissions, workflows |
| [#348](https://github.com/opencode-ai/opencode/pull/348) | Task/TODO system | Scope after stable core and live Qwen verification |

## Original 42 unmerged pull requests

| Original PR | Subject | Triage area | Original head branch |
|---|---|---|---|
| [#348](https://github.com/opencode-ai/opencode/pull/348) | Todo System | UX/agent | `todo-2` |
| [#346](https://github.com/opencode-ai/opencode/pull/346) | Ollama integration | Model/provider | `ollama-integration` |
| [#344](https://github.com/opencode-ai/opencode/pull/344) | Update README.md with Amazon Bedrock | Model/provider | `patch-1` |
| [#336](https://github.com/opencode-ai/opencode/pull/336) | feat(autocompcat): for non interactive mode | General | `feat/compaction-for-non-interactive-mode` |
| [#329](https://github.com/opencode-ai/opencode/pull/329) | Add DeepSeek integration support | Model/provider | `main` |
| [#327](https://github.com/opencode-ai/opencode/pull/327) | fix: typo in keyboard shortcuts window | UX/agent | `fix-typo-in-keyboard-shortcuts-window` |
| [#323](https://github.com/opencode-ai/opencode/pull/323) | add groq Kimi K2 model support | Model/provider | `main` |
| [#316](https://github.com/opencode-ai/opencode/pull/316) | feat: add OpenRouter x-ai/grok-4 model support | Model/provider | `feature/openrouter-grok-4` |
| [#315](https://github.com/opencode-ai/opencode/pull/315) | feat(models): add OpenRouter Kimi K2 model support | Model/provider | `feature/openrouter-kimi-k2` |
| [#314](https://github.com/opencode-ai/opencode/pull/314) | Opencodedigzo.json | General | `patch-1` |
| [#312](https://github.com/opencode-ai/opencode/pull/312) | Adding the grok4 model information to the xai models - verifying info… | Model/provider | `feature/add-grok4-model` |
| [#310](https://github.com/opencode-ai/opencode/pull/310) | feat: add DeepSeek API support | Model/provider | `feat/add-deepseek-api-support` |
| [#308](https://github.com/opencode-ai/opencode/pull/308) | add LOCAL_API_KEY environment variable to support api like ChatAnywhere | Model/provider | `feature/local-third-party-support` |
| [#307](https://github.com/opencode-ai/opencode/pull/307) | feat: add xAI Grok integration with its current features | Model/provider | `main` |
| [#301](https://github.com/opencode-ai/opencode/pull/301) | fix: gemini 429 response | Model/provider | `fix/gemini-25pro` |
| [#294](https://github.com/opencode-ai/opencode/pull/294) | Fix GitHub Copilot authentication flow | Model/provider | `improve-copilot-auth` |
| [#289](https://github.com/opencode-ai/opencode/pull/289) | feat: Transparent theme | UX/agent | `transparent_theme` |
| [#287](https://github.com/opencode-ai/opencode/pull/287) | feat: add claude 4 sonnet/opus to openrouter models | Model/provider | `feature/openrouter-claude-4` |
| [#281](https://github.com/opencode-ai/opencode/pull/281) | fix(mcp): handle empty input by initializing with empty JSON object | Infrastructure | `main` |
| [#272](https://github.com/opencode-ai/opencode/pull/272) | chore: update mcp-go dependency to v0.32.0 | Infrastructure | `mcp` |
| [#268](https://github.com/opencode-ai/opencode/pull/268) | Feature/shell improvements /w Windows support | Infrastructure | `feature/shell-improvements` |
| [#250](https://github.com/opencode-ai/opencode/pull/250) | Add GitHub Action for golangci-lint | Infrastructure | `add-lint` |
| [#249](https://github.com/opencode-ai/opencode/pull/249) | Add dependabot config | Infrastructure | `add-dependabot` |
| [#245](https://github.com/opencode-ai/opencode/pull/245) | feat: Add support for custom provider endpoints and headers | Model/provider | `main` |
| [#243](https://github.com/opencode-ai/opencode/pull/243) | feat(session and litellm): add session deletion flow with Ctrl+P and overlay dialog; support LiteLLM (or any other) proxy; extend vertex models | Model/provider | `feat/delete-session-tui` |
| [#239](https://github.com/opencode-ai/opencode/pull/239) | fix model typo and limit project size in system prompt to 4K max | Model/provider | `limit-project-size` |
| [#238](https://github.com/opencode-ai/opencode/pull/238) | feat(models): add latest openrouter and gemini models | Model/provider | `feature/add-latest-openrouter-models` |
| [#235](https://github.com/opencode-ai/opencode/pull/235) | Add Flake Dev Environment and Optional Package Output | Infrastructure | `main` |
| [#227](https://github.com/opencode-ai/opencode/pull/227) | feat: hide cursor when process loses focus | UX/agent | `schniz/dont-blink-cursor-on-tmux-blur` |
| [#216](https://github.com/opencode-ai/opencode/pull/216) | OpenAI baseUrl support | General | `openai-baseurl-support` |
| [#192](https://github.com/opencode-ai/opencode/pull/192) | feat(vertexai): update Gemini model versions and add new preview models | Model/provider | `vertexai-new-models` |
| [#170](https://github.com/opencode-ai/opencode/pull/170) | Create SECURITY.md | Security | `patch-1` |
| [#167](https://github.com/opencode-ai/opencode/pull/167) | Enhance privacy and security by adding permission checks and improvin… | Security | `enhance-privacy-and-security` |
| [#163](https://github.com/opencode-ai/opencode/pull/163) | docs: fix typos | Documentation | `fix-typos` |
| [#149](https://github.com/opencode-ai/opencode/pull/149) | Support global context paths by merging built-in defaults with user-specified paths | General | `feature/add-support-for-global-context-paths` |
| [#142](https://github.com/opencode-ai/opencode/pull/142) | fix: improve script safety and clarity in path and temp handling | Security | `shell` |
| [#141](https://github.com/opencode-ai/opencode/pull/141) | docs: add Traditional Chinese localization and improve README clarity | Documentation | `docs` |
| [#110](https://github.com/opencode-ai/opencode/pull/110) | chore: adds nix and nixflakes environment | Infrastructure | `chore/dx-nix-dev` |
| [#104](https://github.com/opencode-ai/opencode/pull/104) | feat: add golangci && resolve current lint errors | Infrastructure | `feat/golangci` |
| [#98](https://github.com/opencode-ai/opencode/pull/98) | WIP Provider Config | Model/provider | `openai-compat-providers` |
| [#81](https://github.com/opencode-ai/opencode/pull/81) | Improve language in conversation example about prime | Documentation | `improve-grammar-in-example-about-prime` |
| [#80](https://github.com/opencode-ai/opencode/pull/80) | fix tiny typo, "tune"->"tone" | Documentation | `fix-typo-tune-to-tone` |

## Original 25 branch references

Names and tip SHAs from the source repository at the time of this inventory. These are **not** active DragonForge branches.

| Source branch | Source tip SHA |
|---|---|
| `adam/keybinds` | `f49e37320aa4fb71215d198607dd4cac119590e9` |
| `adam/themes` | `81bb3db9af0d198a3270091fed79c9c0d91cf271` |
| `add-xai` | `0907fedc8d6cb19ea8d962f35b4eb59e1111db0a` |
| `bedrock` | `d83b68f75cf66d4e1c57952303f4d818b74d1205` |
| `bubbletea_v2` | `f5e857bad0547a1d8779c7ce94bdadfb329733c5` |
| `change-db-driver` | `50038e13da65c16a55710d31d0864fc77f57bd42` |
| `cleanup-logs-status` | `3458bcb4c46d717505c273de0fae0dfb2d8916d6` |
| `cleanup-tools` | `e5dd30463c2b17fdf6ee7f3b7c83639719aec404` |
| `feature/context-warning-compact-cmd` | `99b26f5551b2a8ba64521331db2acee1054540ef` |
| `feature/improve-compact` | `6d0f96db6bb528dc3c0d9dab1a0626a7ff7b1e73` |
| `feature/openrouter-deepseek` | `9b2c8f865838debd5c69b16ff5245d4a7cd7f59a` |
| `fix-acc-error` | `463744a3ab03924019a1d7d505d79af180e90eac` |
| `fix-default-config` | `2c1b28a5a331290ef1c5791e075e590f4a54c51d` |
| `fix-gemini` | `c979cac92efa67981c680cc553b0deaef4a8c3f1` |
| `fix-help` | `0d09770baae4bc62dc2990948103d7cffe5d04b4` |
| `fix-kitty` | `d3e49da66dd8c12c441dd20a931872467ff87311` |
| `fix-mcp-tools` | `43774e8497eddf76004aea089d48f496e191fc9d` |
| `fix-warn-message` | `78824e3b93b60c8fd2204e1d4009859e2b65f38e` |
| `main` | `73ee493265acf15fcd8caab2bc8cd3bd375b63cb` |
| `openai-compat-providers` | `4ff4d0428d0cae551e2a946b0753bd6991b28f38` |
| `opencode` | `8e7cb039efbb76361fdceea9a7c4219abf856a1f` |
| `pre-release-fixes` | `380e4c75bf8246f303fd84f699bd6271bb398c5e` |
| `update-gemini-readme` | `72c004c482be9dc845ff8de7c07737085a0c06bf` |
| `update-name` | `ad28ef4fb88b725bcc9f1d991d4dec6c9a845e69` |
| `ux-improvements` | `aedf9960f5a29f45b0f82c27106eab3b8265139c` |

## Testing gate

A port is complete only when it has been adapted to DragonForge's independent module paths, preserves permission boundaries, has new tests for the specific behavior, passes main Go CI and the relevant project integration tests, and is merged through a reviewable PR.
