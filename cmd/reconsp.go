package main

import (
	"fmt"
	"os"
	"ReconSP/internal/orchestrator"
	"ReconSP/pkg/config"
	"ReconSP/pkg/logger"

	"github.com/spf13/cobra"
)

var (
	target string
	depth  int
)

var rootCmd = &cobra.Command{
	Use:   "reconsp",
	Short: "ReconSP - Automated Reconnaissance & Attack Surface Intelligence Tool",
	Long:  `ReconSP is an automated reconnaissance tool designed to discover and analyze the attack surface of a web target.`,
	Run: func(cmd *cobra.Command, args []string) {
		if target == "" {
			fmt.Println("Error: Target URL (e.g., example.com) is required.")
			cmd.Help()
			os.Exit(1)
		}

		// Initialize Logger
		logger.Init(target)

		// Initialize Config (Viper)
		config.Init()

		fmt.Printf("[+] Starting ReconSP for: %s (Depth: %d)\n", target, depth)

		// Initialize Orchestrator and run scan
		orch := orchestrator.NewOrchestrator(target, depth)
		orch.Run()
	},
}

func init() {
	rootCmd.PersistentFlags().StringVarP(&target, "url", "u", "", "Target domain (e.g., example.com)")
	rootCmd.PersistentFlags().IntVarP(&depth, "depth", "d", 1, "Recursive subdomain depth (default: 1)")
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
