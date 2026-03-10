package subdomain

import (
	"fmt"
	"os/exec"
	"strings"
	"ReconSP/pkg/logger"
)

type Enumerator struct {
	Target string
	Depth  int
}

func (e *Enumerator) Enumerate() ([]string, error) {
	fmt.Printf("[+] Starting Subdomain Enumeration for: %s (Depth: %d)\n", e.Target, e.Depth)

	// In a real execution, we would call binaries like subfinder, amass
	// For now, let's implement the 'subfinder' caller as per SRS Section 40
	
	cmd := exec.Command("subfinder", "-d", e.Target, "-silent")
	output, err := cmd.Output()
	if err != nil {
		logger.LogError(fmt.Sprintf("subfinder failed for %s: %v", e.Target, err))
		// Log but perhaps return empty list to not stop whole pipeline
		return nil, nil
	}

	subs := strings.Split(string(output), "\n")
	var cleanedSubs []string
	for _, sub := range subs {
		if sub != "" {
			cleanedSubs = append(cleanedSubs, strings.TrimSpace(sub))
		}
	}

	return cleanedSubs, nil
}
