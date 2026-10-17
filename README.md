# DragonForge Code

🎈 **[Welcome Back, OpenCode!](WELCOME_BACK.md)** — celebrating the historic v0.0.56 milestone and the independent DragonForge revival.

📚 **[Documentation & Wiki Home](docs/WIKI_HOME.md)** — feature inventory, history, and development roadmap.

**Independent, local-first Go coding agent** based on the MIT-licensed OpenCode Go project
and the OpenCode Revival work maintained by HenricHuntsman.

This repository is standalone, not a GitHub fork. Its commit ancestry preserves the
OpenCode Revival and original OpenCode project histories.

## Source and attribution

Original copyright and redistribution conditions are preserved in [LICENSE](LICENSE).
The previous project README is preserved at [docs/OPENCODE-REVIVAL-README.md](docs/OPENCODE-REVIVAL-README.md).

## Build

Requires Go 1.24 or newer.

```bash
go mod verify
go vet ./...
go test ./... -count=1
go build -o dragonforge .
./dragonforge --version
```

The first migration renames the Go module and documentation. The executable,
interface strings, installation and release configurations may still refer to
OpenCode until updated separately. Interactive coding is supported; local Ollama
endpoint is set through `LOCAL_ENDPOINT=http://127.0.0.1:11434/v1`.

Nintendo 64 and TraceForge are isolated specialist workspaces, not merged source
projects. The TraceForge reference workspace must not modify the original project
without permission.

## Historical upstream preservation

The [historical OpenCode archive](docs/upstream/README.md) catalogs the original releases, assets, branches, tags and open pull requests. Historical release copies are labelled separately from DragonForge builds. Check the archive workflow result for transfer status.
