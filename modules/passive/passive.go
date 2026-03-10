package passive

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"time"
	"ReconSP/pkg/logger"
)

type CrtShResult struct {
	IssuerName      string `json:"issuer_name"`
	CommonName      string `json:"common_name"`
	NameValue       string `json:"name_value"`
	Id              int    `json:"id"`
	EntryTimestamp  string `json:"entry_timestamp"`
	NotBefore       string `json:"not_before"`
	NotAfter        string `json:"not_after"`
	SerialNumber    string `json:"serial_number"`
}

func GetCrtShSubdomains(domain string) ([]string, error) {
	fmt.Printf("[+] Querying crt.sh for subdomain intelligence: %s\n", domain)
	url := fmt.Sprintf("https://crt.sh/?q=%%.%s&output=json", domain)

	client := &http.Client{Timeout: 30 * time.Second}
	resp, err := client.Get(url)
	if err != nil {
		logger.LogError(fmt.Sprintf("crt.sh query failed for %s: %v", domain, err))
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return nil, fmt.Errorf("crt.sh returned status code %d", resp.StatusCode)
	}

	var results []CrtShResult
	if err := json.NewDecoder(resp.Body).Decode(&results); err != nil {
		return nil, err
	}

	subdomains := make(map[string]bool)
	for _, res := range results {
		// crt.sh can return multiple values separated by newlines
		names := strings.Split(res.NameValue, "\n")
		for _, name := range names {
			cleanName := strings.TrimPrefix(name, "*.")
			subdomains[strings.ToLower(cleanName)] = true
		}
	}

	var list []string
	for sub := range subdomains {
		list = append(list, sub)
	}

	return list, nil
}
