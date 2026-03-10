package http_module

import (
	"fmt"
	"io"
	"net/http"
	"regexp"
	"strings"
	"time"
	"ReconSP/pkg/logger"
)

type Crawler struct {
	BaseURL string
	Depth   int
}

func NewCrawler(baseURL string, depth int) *Crawler {
	return &Crawler{
		BaseURL: baseURL,
		Depth:   depth,
	}
}

func (c *Crawler) Crawl() ([]string, error) {
	fmt.Printf("[+] Crawling: %s\n", c.BaseURL)

	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Get(c.BaseURL)
	if err != nil {
		logger.LogError("Crawl failed: " + err.Error())
		return nil, err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	// Regex for link extraction
	linkRE := regexp.MustCompile(`href=["'](https?://[^"']+|/[^"']+)["']`)
	matches := linkRE.FindAllStringSubmatch(string(body), -1)

	var links []string
	seen := make(map[string]bool)
	for _, m := range matches {
		link := m[1]
		if strings.HasPrefix(link, "/") {
			link = strings.TrimSuffix(c.BaseURL, "/") + link
		}
		if !seen[link] {
			links = append(links, link)
			seen[link] = true
		}
	}

	return links, nil
}
