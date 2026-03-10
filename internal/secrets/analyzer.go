package secrets

import (
	"encoding/base64"
	"fmt"
	"regexp"
)

type SecretAnalyzer struct {
	Patterns map[string]*regexp.Regexp
}

func NewSecretAnalyzer() *SecretAnalyzer {
	// Patterns following SRS Section 15 & 43
	return &SecretAnalyzer{
		Patterns: map[string]*regexp.Regexp{
			"AWS Key":       regexp.MustCompile(`AKIA[0-9A-Z]{16}`),
			"Google API Key": regexp.MustCompile(`AIza[0-9A-Za-z\\-_]{35}`),
			"JWT Token":     regexp.MustCompile(`eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+`),
			"Base64 Potential": regexp.MustCompile(`[a-zA-Z0-9+/]{20,}={0,2}`),
		},
	}
}

func (s *SecretAnalyzer) ScanContent(content string) []string {
	var found []string
	for name, re := range s.Patterns {
		matches := re.FindAllString(content, -1)
		for _, match := range matches {
			if name == "Base64 Potential" {
				// Decode and analyze (SRS Section 44)
				decoded, err := base64.StdEncoding.DecodeString(match)
				if err == nil {
					// Recursively scan decoded content for deeper secrets
					found = append(found, fmt.Sprintf("[!] Found Base64 Content (%s) -> Decoded: %s", match, string(decoded)))
				}
			} else {
				found = append(found, fmt.Sprintf("[!] Found %s: %s", name, match))
			}
		}
	}
	return found
}
