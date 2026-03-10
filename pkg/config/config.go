package config

import (
	"fmt"

	"github.com/spf13/viper"
)

type Config struct {
	RateLimit          int    `mapstructure:"rate_limit"`
	MaxWorkers         int    `mapstructure:"max_workers"`
	DepthLimit         int    `mapstructure:"depth_limit"`
	EnableCloudScan    bool   `mapstructure:"enable_cloud_scan"`
	EnableTakeoverScan bool   `mapstructure:"enable_takeover_scan"`
	Proxy              string `mapstructure:"proxy"`
}

var AppConfig Config

func Init() {
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath("configs")

	// Set Defaults as per SRS Section 36
	viper.SetDefault("rate_limit", 100)
	viper.SetDefault("max_workers", 50)
	viper.SetDefault("depth_limit", 3)
	viper.SetDefault("enable_cloud_scan", true)
	viper.SetDefault("enable_takeover_scan", true)

	// Environment Variables support
	viper.AutomaticEnv()

	if err := viper.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			// Config file not found; ignore error if desired
			fmt.Println("[!] Config file not found, using defaults.")
		} else {
			// Config file was found but another error was produced
			fmt.Printf("[!] Error reading config: %v\n", err)
		}
	}

	if err := viper.Unmarshal(&AppConfig); err != nil {
		fmt.Printf("[!] Unable to decode config into struct: %v\n", err)
	}
}
