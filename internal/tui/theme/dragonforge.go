package theme

import (
	"github.com/charmbracelet/lipgloss"
)

// DragonForgeTheme implements the Theme interface with DragonForge dragon-inspired colors.
// It provides both dark and light variants, though Tron is primarily a dark theme.
type DragonForgeTheme struct {
	BaseTheme
}

// NewDragonForgeTheme creates a new instance of the DragonForge theme.
func NewDragonForgeTheme() *DragonForgeTheme {
	// DragonForge flame and code palette
	// Inspired by the original DragonForge dragon icons: orange eyes, cyan code, deep navy surfaces
	darkBackground := "#0b1220"
	darkCurrentLine := "#1b293b"
	darkSelection := "#1b293b"
	darkForeground := "#eef5ff"
	darkComment := "#8fa3bf"
	darkCyan := "#18c5ff"
	darkBlue := "#368bff"
	darkOrange := "#ff7518"
	darkPink := "#ef64b9"
	darkPurple := "#a768ff"
	darkRed := "#ff5b66"
	darkYellow := "#ffc247"
	darkGreen := "#21dca8"
	darkBorder := "#1b293b"

	// Light mode approximation
	lightBackground := "#f5f7fb"
	lightCurrentLine := "#e8eef7"
	lightSelection := "#d4e3f7"
	lightForeground := "#0b1220"
	lightComment := "#8fa3bf"
	lightCyan := "#007a9e"
	lightBlue := "#2369bc"
	lightOrange := "#b55300"
	lightPink := "#b3247f"
	lightPurple := "#6b42c5"
	lightRed := "#b93142"
	lightYellow := "#a46b00"
	lightGreen := "#007e59"
	lightBorder := "#d4e3f7"

	theme := &DragonForgeTheme{}

	// Base colors
	theme.PrimaryColor = lipgloss.AdaptiveColor{
		Dark:  darkCyan,
		Light: lightCyan,
	}
	theme.SecondaryColor = lipgloss.AdaptiveColor{
		Dark:  darkBlue,
		Light: lightBlue,
	}
	theme.AccentColor = lipgloss.AdaptiveColor{
		Dark:  darkOrange,
		Light: lightOrange,
	}

	// Status colors
	theme.ErrorColor = lipgloss.AdaptiveColor{
		Dark:  darkRed,
		Light: lightRed,
	}
	theme.WarningColor = lipgloss.AdaptiveColor{
		Dark:  darkOrange,
		Light: lightOrange,
	}
	theme.SuccessColor = lipgloss.AdaptiveColor{
		Dark:  darkGreen,
		Light: lightGreen,
	}
	theme.InfoColor = lipgloss.AdaptiveColor{
		Dark:  darkCyan,
		Light: lightCyan,
	}

	// Text colors
	theme.TextColor = lipgloss.AdaptiveColor{
		Dark:  darkForeground,
		Light: lightForeground,
	}
	theme.TextMutedColor = lipgloss.AdaptiveColor{
		Dark:  darkComment,
		Light: lightComment,
	}
	theme.TextEmphasizedColor = lipgloss.AdaptiveColor{
		Dark:  darkYellow,
		Light: lightYellow,
	}

	// Background colors
	theme.BackgroundColor = lipgloss.AdaptiveColor{
		Dark:  darkBackground,
		Light: lightBackground,
	}
	theme.BackgroundSecondaryColor = lipgloss.AdaptiveColor{
		Dark:  darkCurrentLine,
		Light: lightCurrentLine,
	}
	theme.BackgroundDarkerColor = lipgloss.AdaptiveColor{
		Dark:  "#070b14", // Slightly darker than background
		Light: "#ffffff", // Slightly lighter than background
	}

	// Border colors
	theme.BorderNormalColor = lipgloss.AdaptiveColor{
		Dark:  darkBorder,
		Light: lightBorder,
	}
	theme.BorderFocusedColor = lipgloss.AdaptiveColor{
		Dark:  darkCyan,
		Light: lightCyan,
	}
	theme.BorderDimColor = lipgloss.AdaptiveColor{
		Dark:  darkSelection,
		Light: lightSelection,
	}

	// Diff view colors
	theme.DiffAddedColor = lipgloss.AdaptiveColor{
		Dark:  darkGreen,
		Light: lightGreen,
	}
	theme.DiffRemovedColor = lipgloss.AdaptiveColor{
		Dark:  darkRed,
		Light: lightRed,
	}
	theme.DiffContextColor = lipgloss.AdaptiveColor{
		Dark:  darkComment,
		Light: lightComment,
	}
	theme.DiffHunkHeaderColor = lipgloss.AdaptiveColor{
		Dark:  darkBlue,
		Light: lightBlue,
	}
	theme.DiffHighlightAddedColor = lipgloss.AdaptiveColor{
		Dark:  "#21dca8",
		Light: "#a5d6a7",
	}
	theme.DiffHighlightRemovedColor = lipgloss.AdaptiveColor{
		Dark:  "#ff5b66",
		Light: "#ef9a9a",
	}
	theme.DiffAddedBgColor = lipgloss.AdaptiveColor{
		Dark:  "#102b26",
		Light: "#e8f5e9",
	}
	theme.DiffRemovedBgColor = lipgloss.AdaptiveColor{
		Dark:  "#301923",
		Light: "#ffebee",
	}
	theme.DiffContextBgColor = lipgloss.AdaptiveColor{
		Dark:  darkBackground,
		Light: lightBackground,
	}
	theme.DiffLineNumberColor = lipgloss.AdaptiveColor{
		Dark:  darkComment,
		Light: lightComment,
	}
	theme.DiffAddedLineNumberBgColor = lipgloss.AdaptiveColor{
		Dark:  "#0c2721",
		Light: "#c8e6c9",
	}
	theme.DiffRemovedLineNumberBgColor = lipgloss.AdaptiveColor{
		Dark:  "#261017",
		Light: "#ffcdd2",
	}

	// Markdown colors
	theme.MarkdownTextColor = lipgloss.AdaptiveColor{
		Dark:  darkForeground,
		Light: lightForeground,
	}
	theme.MarkdownHeadingColor = lipgloss.AdaptiveColor{
		Dark:  darkCyan,
		Light: lightCyan,
	}
	theme.MarkdownLinkColor = lipgloss.AdaptiveColor{
		Dark:  darkBlue,
		Light: lightBlue,
	}
	theme.MarkdownLinkTextColor = lipgloss.AdaptiveColor{
		Dark:  darkCyan,
		Light: lightCyan,
	}
	theme.MarkdownCodeColor = lipgloss.AdaptiveColor{
		Dark:  darkGreen,
		Light: lightGreen,
	}
	theme.MarkdownBlockQuoteColor = lipgloss.AdaptiveColor{
		Dark:  darkYellow,
		Light: lightYellow,
	}
	theme.MarkdownEmphColor = lipgloss.AdaptiveColor{
		Dark:  darkYellow,
		Light: lightYellow,
	}
	theme.MarkdownStrongColor = lipgloss.AdaptiveColor{
		Dark:  darkOrange,
		Light: lightOrange,
	}
	theme.MarkdownHorizontalRuleColor = lipgloss.AdaptiveColor{
		Dark:  darkComment,
		Light: lightComment,
	}
	theme.MarkdownListItemColor = lipgloss.AdaptiveColor{
		Dark:  darkBlue,
		Light: lightBlue,
	}
	theme.MarkdownListEnumerationColor = lipgloss.AdaptiveColor{
		Dark:  darkCyan,
		Light: lightCyan,
	}
	theme.MarkdownImageColor = lipgloss.AdaptiveColor{
		Dark:  darkBlue,
		Light: lightBlue,
	}
	theme.MarkdownImageTextColor = lipgloss.AdaptiveColor{
		Dark:  darkCyan,
		Light: lightCyan,
	}
	theme.MarkdownCodeBlockColor = lipgloss.AdaptiveColor{
		Dark:  darkForeground,
		Light: lightForeground,
	}

	// Syntax highlighting colors
	theme.SyntaxCommentColor = lipgloss.AdaptiveColor{
		Dark:  darkComment,
		Light: lightComment,
	}
	theme.SyntaxKeywordColor = lipgloss.AdaptiveColor{
		Dark:  darkCyan,
		Light: lightCyan,
	}
	theme.SyntaxFunctionColor = lipgloss.AdaptiveColor{
		Dark:  darkGreen,
		Light: lightGreen,
	}
	theme.SyntaxVariableColor = lipgloss.AdaptiveColor{
		Dark:  darkOrange,
		Light: lightOrange,
	}
	theme.SyntaxStringColor = lipgloss.AdaptiveColor{
		Dark:  darkYellow,
		Light: lightYellow,
	}
	theme.SyntaxNumberColor = lipgloss.AdaptiveColor{
		Dark:  darkBlue,
		Light: lightBlue,
	}
	theme.SyntaxTypeColor = lipgloss.AdaptiveColor{
		Dark:  darkPurple,
		Light: lightPurple,
	}
	theme.SyntaxOperatorColor = lipgloss.AdaptiveColor{
		Dark:  darkPink,
		Light: lightPink,
	}
	theme.SyntaxPunctuationColor = lipgloss.AdaptiveColor{
		Dark:  darkForeground,
		Light: lightForeground,
	}

	return theme
}

func init() {
	// Register the DragonForge theme with the theme manager
	RegisterTheme("dragonforge", NewDragonForgeTheme())
}
