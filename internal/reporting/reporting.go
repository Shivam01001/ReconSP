package reporting

import (
	"html/template"
	"os"
	"path/filepath"
	"ReconSP/pkg/logger"
)

type ReportData struct {
	Target          string
	ScanDate        string
	SubdomainCount  int
	VulnerabilityCount int
	RiskScore       string
	Subdomains      []SubdomainInfo
	Vulnerabilities []VulnerabilityInfo
}

type SubdomainInfo struct {
	Host       string
	IP         string
	Status     string
	Server     string
	TechStack  string
}

type VulnerabilityInfo struct {
	Name        string
	Severity    string
	Description string
	Target      string
}

func GenerateHTMLReport(target string, data ReportData) error {
	templatePath := filepath.Join("templates", "report.html")
	outputPath := filepath.Join("logs", target, "report.html")

	tmpl, err := template.ParseFiles(templatePath)
	if err != nil {
		logger.LogError("Failed to parse report template: " + err.Error())
		return err
	}

	file, err := os.Create(outputPath)
	if err != nil {
		logger.LogError("Failed to create report file: " + err.Error())
		return err
	}
	defer file.Close()

	if err := tmpl.Execute(file, data); err != nil {
		logger.LogError("Failed to execute report template: " + err.Error())
		return err
	}

	return nil
}
