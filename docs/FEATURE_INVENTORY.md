# DragonForge — Feature Inventory

This is a **documentation starting point**, not a fresh end-to-end test report.

| Area | Known project context | Verification needed |
| --- | --- | --- |
| Interactive terminal coding agent | Core OpenCode Go foundation | Launch and interactive workflow |
| AI agent and coding tools | Inherited project functionality | Read/edit/write/execute tests and permission checks |
| Provider and local endpoint support | README documents LOCAL_ENDPOINT | Ollama/Qwen live request and response |
| MCP/tool calling | Historical revival work includes tool-call fixes | Parameterless and parameterized tool regression tests |
| Sessions and context | Historical OpenCode functionality | Persistence and recovery |
| Themes, shortcuts, navigation | Historical terminal interface work | Runtime UI test |
| Historical releases and branches | Archive index exists | Check archive workflow and asset integrity |
| ForgeTerminal integration | Proposed | Design and adapter test |
| Greenlight integration | Separate project; proposed workflow | Explicit integration design |
| Nintendo 64 and TraceForge | Isolated specialist workspaces per README | Keep separate until independently verified |

## Baseline verification

From a clean, compatible Go environment:

```bash
go mod verify
go vet ./...
go test ./... -count=1
go build -o dragonforge .
./dragonforge --version
```

Record actual command outputs and dates in subsequent verification reports. Historical reports do not replace fresh tests.
