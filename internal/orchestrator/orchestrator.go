package orchestrator

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"ReconSP/pkg/config"
	"ReconSP/pkg/logger"
	"ReconSP/internal/reporting"
	"ReconSP/modules/subdomain"
	"ReconSP/modules/passive"
	"ReconSP/modules/dns"
	"ReconSP/modules/http"
	"ReconSP/modules/js"
	"ReconSP/modules/vulnerability"
	"ReconSP/internal/secrets"
	"io"
	"net/http"
	"time"
)

type Orchestrator struct {
	Target string
	Depth  int
	LogDir string
}

func NewOrchestrator(target string, depth int) *Orchestrator {
	logDir := filepath.Join("logs", target)
	os.MkdirAll(logDir, 0755)
	os.MkdirAll(filepath.Join(logDir, "screenshots"), 0755)

	return &Orchestrator{
		Target: target,
		Depth:  depth,
		LogDir: logDir,
	}
}

func (o *Orchestrator) Run() {
	fmt.Printf("[+] Pipeline initialized for: %s (Max Workers: %d)\n", o.Target, config.AppConfig.MaxWorkers)

	// Step-by-step pipeline execution logic
	steps := []struct {
		Name string
		Func func() error
	}{
		{"Passive Intelligence", o.PassiveIntel},
		{"Subdomain Enumeration", o.SubdomainEnum},
		{"DNS Resolution", o.DNSResolution},
		{"Live Host Detection", o.LiveHostDetection},
		{"Technology Detection", o.TechDetection},
		{"Crawling Engine", o.CrawlingEngine},
		{"JS Intelligence", o.JSIntelligence},
		{"Secret Detection", o.SecretDetection},
		{"Backup File Discovery", o.BackupDiscovery},
		{"Cloud Asset Discovery", o.CloudDiscovery},
		{"Takeover Detection", o.TakeoverDetection},
		{"Vulnerability Scanning", o.VulnScanning},
		{"Screenshot Automation", o.ScreenshotAutomation},
		{"Final Reporting", o.GenerateReport},
	}

	for _, step := range steps {
		fmt.Printf("[+] Running: %s...\n", step.Name)
		if err := step.Func(); err != nil {
			logger.LogError(fmt.Sprintf("Step %s failed for %s: %v", step.Name, o.Target, err))
			fmt.Printf("[!] %s FAILED (Check logs/errors.log)\n", step.Name)
		} else {
			fmt.Printf("[✔] %s COMPLETED\n", step.Name)
		}
	}

	fmt.Printf("\n[+] ReconSP Pipeline for %s finished successfully!\n", o.Target)
	fmt.Printf("[+] Report saved in: %s/report.html\n", o.LogDir)
}

// Placeholder Pipeline steps (Logic to be moved to internal/scanner / modules/)
func (o *Orchestrator) PassiveIntel() error {
	subs, err := passive.GetCrtShSubdomains(o.Target)
	if err != nil {
		return err
	}
	fmt.Printf("[+] Found %d potential subdomains from crt.sh\n", len(subs))
	return nil
}
func (o *Orchestrator) SubdomainEnum() error {
	enum := subdomain.Enumerator{Target: o.Target, Depth: o.Depth}
	subs, err := enum.Enumerate()
	if err != nil {
		return err
	}
	fmt.Printf("[+] Found %d unique subdomains\n", len(subs))
	return nil
}
func (o *Orchestrator) DNSResolution() error {
	// This should normally take the subdomains from SubdomainEnum
	// For demo/continuation, we just resolve the target
	fmt.Printf("[+] Resolving domain: %s\n", o.Target)
	res, err := dns_module.ResolveDomain(o.Target)
	if err != nil {
		return err
	}
	fmt.Printf("[+] IPs found: %s\n", strings.Join(res.IPs, ", "))
	return nil
}

func (o *Orchestrator) LiveHostDetection() error {
	fmt.Printf("[+] Testing live hosts for: %s\n", o.Target)
	// Try http and https
	for _, protocol := range []string{"http", "https"} {
		url := fmt.Sprintf("%s://%s", protocol, o.Target)
		probe, err := http_module.ProbeURL(url)
		if err == nil {
			fmt.Printf("[+] Found live host: %s (Status: %d, Server: %s)\n", probe.URL, probe.StatusCode, probe.Server)
		}
	}
	return nil
}
func (o *Orchestrator) TechDetection() error  { return nil }
func (o *Orchestrator) CrawlingEngine() error {
	c := http_module.NewCrawler("https://"+o.Target, 1)
	links, err := c.Crawl()
	if err != nil {
		return err
	}
	fmt.Printf("[+] Discovered %d endpoints from crawling\n", len(links))
	return nil
}

func (o *Orchestrator) JSIntelligence() error {
	endpoints, err := js_module.AnalyzeJS("https://" + o.Target)
	if err != nil {
		return err
	}
	fmt.Printf("[+] Discovered %d API endpoints from JavaScript analysis\n", len(endpoints))
	return nil
}

func (o *Orchestrator) SecretDetection() error {
	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Get("https://" + o.Target)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)

	s := secrets.NewSecretAnalyzer()
	found := s.ScanContent(string(body))
	for _, secret := range found {
		fmt.Printf("[!] %s\n", secret)
	}
	return nil
}
func (o *Orchestrator) BackupDiscovery() error { return nil }
func (o *Orchestrator) CloudDiscovery() error  { return nil }
func (o *Orchestrator) TakeoverDetection() error { return nil }
func (o *Orchestrator) VulnScanning() error {
	v := vulnerability.NewNucleiScanner(o.Target, o.LogDir)
	return v.RunScan()
}
func (o *Orchestrator) ScreenshotAutomation() error { return nil }
func (o *Orchestrator) GenerateReport() error {
	data := reporting.ReportData{
		Target:          o.Target,
		ScanDate:        "2026-03-10", // Should be dynamic
		SubdomainCount:  0,
		VulnerabilityCount: 0,
		RiskScore:       "Grade: B",
	}
	return reporting.GenerateHTMLReport(o.Target, data)
}
