package js_module

import (
	"fmt"
	"io"
	"net/http"
	"regexp"
	"strings"
	"time"
)

type JSAnalyzer struct {
	Target string
}

func AnalyzeJS(baseURL string) ([]string, error) {
	fmt.Printf("[+] Analyzing JavaScript on: %s\n", baseURL)

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Get(baseURL)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	// Regex for JS Files
	jsRE := regexp.MustCompile(`<script.*?src=["'](.*?.js.*?)["']`)
	matches := jsRE.FindAllStringSubmatch(string(body), -1)

	var endpoints []string
	for _, m := range matches {
		jsURL := m[1]
		if !strings.HasPrefix(jsURL, "http") {
			jsURL = strings.TrimSuffix(baseURL, "/") + "/" + strings.TrimPrefix(jsURL, "/")
		}
		// Try to find API endpoints in JS using regex (simplified)
		apiRE := regexp.MustCompile(`/(?:api|v[0-9])/[\w\-./]+`)
		jsContent, _ := fetchJS(jsURL)
		if jsContent != "" {
			apiMatches := apiRE.FindAllString(jsContent, -1)
			endpoints = append(endpoints, apiMatches...)
		}
	}

	return endpoints, nil
}

func fetchJS(url string) (string, error) {
	client := &http.Client{Timeout: 5 * time.Second}
	resp, err := client.Get(url)
	if err != nil || resp.StatusCode != 200 {
		return "", err
	}
	defer resp.Body.Close()
	body, _ := io.ReadAll(resp.Body)
	return string(body), nil
}
