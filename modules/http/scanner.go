package http_module

import (
	"net/http"
	"time"
)

type HostProbe struct {
	URL           string
	StatusCode    int
	ContentLength int64
	Title         string
	Server        string
	Technologies  []string
}

func ProbeURL(targetURL string) (*HostProbe, error) {
	client := &http.Client{
		Timeout: 5 * time.Second,
		// No redirect logic as per section 11
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			return http.ErrUseLastResponse
		},
	}

	resp, err := client.Get(targetURL)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	probeResult := &HostProbe{
		URL:           targetURL,
		StatusCode:    resp.StatusCode,
		ContentLength: resp.ContentLength,
		Server:        resp.Header.Get("Server"),
	}

	// Tech fingerprinting (Section 12)
	if resp.Header.Get("X-Powered-By") != "" {
		probeResult.Technologies = append(probeResult.Technologies, resp.Header.Get("X-Powered-By"))
	}
	// Add more complex detection here

	return probeResult, nil
}
