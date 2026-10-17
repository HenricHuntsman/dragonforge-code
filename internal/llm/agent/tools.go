package agent

import (
	"context"
	"os"

	"github.com/HenricHuntsman/dragonforge-code/internal/config"
	"github.com/HenricHuntsman/dragonforge-code/internal/history"
	"github.com/HenricHuntsman/dragonforge-code/internal/llm/tools"
	"github.com/HenricHuntsman/dragonforge-code/internal/logging"
	"github.com/HenricHuntsman/dragonforge-code/internal/lsp"
	"github.com/HenricHuntsman/dragonforge-code/internal/message"
	"github.com/HenricHuntsman/dragonforge-code/internal/permission"
	"github.com/HenricHuntsman/dragonforge-code/internal/session"
	"github.com/HenricHuntsman/dragonforge-code/internal/skills"
)

func CoderAgentTools(
	permissions permission.Service,
	sessions session.Service,
	messages message.Service,
	history history.Service,
	lspClients map[string]*lsp.Client,
) []tools.BaseTool {
	ctx := context.Background()
	otherTools := GetMcpTools(ctx, permissions)
	if len(lspClients) > 0 {
		otherTools = append(otherTools, tools.NewDiagnosticsTool(lspClients))
	}
	if found := discoverSkills(); len(found) > 0 {
		otherTools = append(otherTools, tools.NewSkillTool(found))
	}
	return append(
		[]tools.BaseTool{
			tools.NewBashTool(permissions),
			tools.NewEditTool(lspClients, permissions, history),
			tools.NewFetchTool(permissions),
			tools.NewGlobTool(),
			tools.NewGrepTool(),
			tools.NewLsTool(),
			tools.NewSourcegraphTool(),
			tools.NewViewTool(lspClients),
			tools.NewPatchTool(lspClients, permissions, history),
			tools.NewWriteTool(lspClients, permissions, history),
			NewAgentTool(sessions, messages, lspClients),
		}, otherTools...,
	)
}

func discoverSkills() []skills.Skill {
	home, _ := os.UserHomeDir()
	found, warnings := skills.Discover(config.WorkingDirectory(), home)
	for _, w := range warnings {
		logging.Warn("Skipping invalid skill: %s", w)
	}
	return found
}

func TaskAgentTools(lspClients map[string]*lsp.Client) []tools.BaseTool {
	return []tools.BaseTool{
		tools.NewGlobTool(),
		tools.NewGrepTool(),
		tools.NewLsTool(),
		tools.NewSourcegraphTool(),
		tools.NewViewTool(lspClients),
	}
}
