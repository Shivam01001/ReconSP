package dns_module

import (
	"fmt"
	"net"
	"strings"
	"ReconSP/pkg/logger"
)

type DNSResult struct {
	Domain string
	IPs    []string
	CNAME  string
}

func ResolveDomain(domain string) (*DNSResult, error) {
	result := &DNSResult{Domain: domain}

	// Resolve A records
	ips, err := net.LookupIP(domain)
	if err != nil {
		logger.LogError(fmt.Sprintf("DNS lookup failed for %s: %v", domain, err))
		return nil, err
	}

	for _, ip := range ips {
		result.IPs = append(result.IPs, ip.String())
	}

	// Resolve CNAME
	cname, err := net.LookupCNAME(domain)
	if err == nil {
		result.CNAME = strings.TrimSuffix(cname, ".")
	}

	return result, nil
}
