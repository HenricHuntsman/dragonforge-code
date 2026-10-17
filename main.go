package main

import (
	"github.com/HenricHuntsman/dragonforge-code/cmd"
	"github.com/HenricHuntsman/dragonforge-code/internal/logging"
)

func main() {
	defer logging.RecoverPanic("main", func() {
		logging.ErrorPersist("Application terminated due to unhandled panic")
	})

	cmd.Execute()
}
